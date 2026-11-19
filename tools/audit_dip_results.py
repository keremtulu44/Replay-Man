"""Dip çıktılarının hash, bölüm, örneklem ve fiyat aritmetiği tutarlılığını denetle.

Bu, bağımsız piyasa kaynağı denetimi veya finansal başarı testi değildir.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from replayman.replay import load_bars
from tools.measure_dip_pilot import load_benchmarks, load_external, sha256, summarize_outcomes, summarize_signals


def require(condition, message: str) -> None:
    if not bool(condition):
        raise ValueError(message)


def verify_hashes(directory: Path) -> int:
    meta = json.loads((directory / "run_metadata.json").read_text(encoding="utf-8"))
    for name, digest in meta["code_sha256"].items():
        require(Path(name).is_file() and sha256(Path(name)) == digest, f"Kod/plan hash uyuşmazlığı: {name}")
    inputs = pd.read_csv(directory / "input_manifest.csv")
    for row in inputs.itertuples():
        source = Path(row.path)
        require(source.is_file() and sha256(source) == row.sha256, f"Girdi hash uyuşmazlığı: {source}")
    return len(inputs)


def verify_summaries(directory: Path, signals: pd.DataFrame, outcomes: pd.DataFrame, pivots: pd.DataFrame) -> None:
    pairs = [(summarize_signals(signals, pivots), pd.read_csv(directory / "signal_summary.csv")),
             (summarize_outcomes(outcomes), pd.read_csv(directory / "outcome_summary.csv"))]
    for actual, saved in pairs:
        pd.testing.assert_frame_equal(actual.reset_index(drop=True), saved.reset_index(drop=True), check_dtype=False,
                                      check_exact=False, rtol=1e-9, atol=1e-12)


def verify_relations(signals: pd.DataFrame, outcomes: pd.DataFrame, pivots: pd.DataFrame, *, external: bool) -> dict:
    require(signals.signal_id.is_unique, "Sinyal kimlikleri tekil değil")
    keys = ["asset_id", "interval", "period", "signal_position"]
    key_set = lambda frame: set(map(tuple, frame[keys].itertuples(index=False, name=None)))
    all_a = key_set(signals.loc[signals.variant == "A_all"])
    without = key_set(signals.loc[signals.variant == "A_no_support"])
    with_zone = key_set(signals.loc[signals.variant == "B_support"])
    require(not (without & with_zone) and all_a == without | with_zone, "A destek alt-kümeleri bölünmüyor")
    support = signals.loc[signals.variant == "B_support"]
    require((support.zone_created_position < support.signal_position).all(), "Destek aynı/sonraki bardan alınmış")
    c = signals.loc[signals.variant == "C_confirmed"]
    origins = set(zip(c.asset_id, c.interval, c.period, c.origin_position.astype(int)))
    require(origins <= with_zone, "C teyidi aynı bölümdeki B adayından gelmiyor")
    require((c.signal_position > c.origin_position).all(), "C teyit tarihi öncesinde yayınlanmış")
    matches = signals.loc[signals.label_status == "matched"].merge(
        pivots, left_on=["asset_id", "interval", "period", "matched_pivot_position"],
        right_on=["asset_id", "interval", "period", "pivot_position"], how="left", validate="many_to_one")
    require(matches.pivot_position.notna().all(), "Eşleşen sinyalin referans dibi yok")
    require(((matches.signal_position >= matches.pivot_position - 2) &
             (matches.signal_position <= matches.pivot_position + 3)).all(), "Dip etiket zaman aralığı geçersiz")
    gap = matches.signal_close - matches.pivot_low
    require(((gap >= -1e-10) & (gap <= matches.atr + 1e-10)).all(), "Dip/ATR mesafesi hatalı")
    require(len(outcomes) == 4 * len(signals), "Her sinyal için iki giriş ve iki ufuk yok")
    require(outcomes.groupby("signal_id").size().eq(4).all(), "Sinyal başına sonuç sayısı hatalı")
    valid = outcomes.loc[outcomes.status == "observed"]
    require((valid.entry_position <= valid.exit_position).all() and (valid.exit_position <= valid.end_position).all(),
            "Stop/hedef sonuç penceresi geçersiz")
    require((valid.trade_lower <= valid.trade_upper + 1e-12).all(), "Belirsiz işlem alt/üst sırası ters")
    other = outcomes.loc[outcomes.status != "observed"]
    require(other.fixed_return.isna().all() and other.excess_return.isna().all(), "Sansürlü sonuç sayısal yazılmış")
    if external:
        require(outcomes.benchmark_return.isna().all() and outcomes.excess_return.isna().all(),
                "Harici arşive doğrulanmamış benchmark eklenmiş")
    return {"signals": len(signals), "outcomes": len(outcomes), "matched_signals": len(matches),
            "observed": len(valid), "censored_or_unknown": len(other)}


def spot_check(directory: Path, outcomes: pd.DataFrame, *, external: bool, count: int = 200) -> int:
    source_files = pd.read_csv(directory / "input_manifest.csv")
    mapping = {(r.asset_id, r.interval): Path(r.path) for r in source_files.itertuples() if r.kind != "benchmark"}
    benchmark = {} if external else load_benchmarks(Path("data/ohlcv"))[0]
    cache: dict[tuple[str, str], pd.DataFrame] = {}
    observed = outcomes.loc[outcomes.status == "observed"]
    sample = observed.sample(min(count, len(observed)), random_state=413)
    for row in sample.itertuples():
        key = (row.asset_id, row.interval)
        if key not in cache:
            cache[key] = load_external(mapping[key])[0] if external else load_bars(mapping[key])
        bars = cache[key]
        entry, end = int(row.entry_position), int(row.end_position)
        require(end - entry + 1 == row.horizon, "Sonuç ufku hatalı")
        require(pd.Timestamp(row.entry_ts) == bars.ts_utc.iloc[entry] and pd.Timestamp(row.end_ts) == bars.ts_utc.iloc[end],
                "Giriş/bitiş bar etiketi uyuşmuyor")
        actual = float(bars.close.iloc[end]) / float(bars.open.iloc[entry]) - 1
        require(np.isclose(row.fixed_return, actual, rtol=1e-10, atol=1e-10), "Sabit ufuk aritmetiği uyuşmuyor")
        if not external:
            market = benchmark.get(row.interval)
            if market is not None and bars.ts_utc.iloc[entry] in market.index and bars.ts_utc.iloc[end] in market.index:
                market_return = float(market.at[bars.ts_utc.iloc[end], "close"]) / float(market.at[bars.ts_utc.iloc[entry], "open"]) - 1
                require(np.isclose(row.benchmark_return, market_return, rtol=1e-10, atol=1e-10), "XU100 başlangıç/bitiş eşleşmesi hatalı")
                require(np.isclose(row.excess_return, actual - market_return, rtol=1e-10, atol=1e-10), "Endeks farkı aritmetiği hatalı")
            else:
                require(pd.isna(row.benchmark_return) and pd.isna(row.excess_return), "Eksik XU100 sıfır sayılmış")
    return len(sample)


def audit(root: Path) -> dict:
    result = {"audited_at_utc": datetime.now(timezone.utc).isoformat(),
              "scope": "artifact integrity and sample arithmetic; not provider independence or performance proof", "sources": {}}
    for source in ("internal", "external"):
        directory = root / source
        count = verify_hashes(directory)
        signals, outcomes, pivots = (pd.read_csv(directory / name) for name in ("signals.csv", "outcomes.csv", "reference_pivots.csv"))
        info = verify_relations(signals, outcomes, pivots, external=(source == "external"))
        verify_summaries(directory, signals, outcomes, pivots)
        info["input_files_verified"] = count
        info["spot_checked_observed_outcomes"] = spot_check(directory, outcomes, external=(source == "external"))
        info["status"] = "passed"
        result["sources"][source] = info
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--research", type=Path, default=Path("research/measurements/dip-research"))
    args = parser.parse_args()
    result = audit(args.research)
    (args.research / "AUDIT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
