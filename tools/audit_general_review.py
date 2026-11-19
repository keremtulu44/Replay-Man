"""Genel denetimdeki eşleşme, zaman, hash ve fiyat aritmetiği kontrolü."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from replayman.acceptance_review import down_acceptance_representatives
from replayman.contemporaneous_control import bar_context
from replayman.dip_research import Period, period_at
from replayman.general_review import week_starts
from replayman.replay import causal_features, load_bars
from replayman.structure import structure_events
from replayman.swings import SwingConfig, confirmed_swings
from tools.audit_dip_results import require, verify_hashes
from tools.audit_legacy_alignment import window_alignment
from tools.compare_dip_contemporaneous import summarize as summarize_contemporaneous
from tools.measure_dip_pilot import EXTERNAL_PERIODS, INTERNAL_PERIODS, load_external, sha256
from tools.review_acceptance_candidate import summarize as summarize_acceptance
from tools.review_general_results import external_stability, summarize_controls, summarize_p6, verified_markets


def verify_metadata(output: Path, research: Path) -> None:
    for name in ("run_metadata.json", "contemporaneous_metadata.json", "acceptance_metadata.json"):
        meta = json.loads((output / name).read_text(encoding="utf-8"))
        for key in ("code_sha256", "source_file_sha256"):
            for path, digest in meta[key].items():
                target = Path(path)
                require(target.is_file() and sha256(target) == digest, f"{name}: kaynak hash uyuşmuyor: {path}")
        for path, digest in meta["output_file_sha256"].items():
            target = output / path
            require(target.is_file() and sha256(target) == digest, f"{name}: çıktı hash uyuşmuyor: {path}")
    meta = json.loads((output / "legacy_alignment_metadata.json").read_text(encoding="utf-8"))
    require(meta["plan_sha256"] == sha256(Path("research/measurements/general-review/PLAN.md")), "Eski hizalama planı uyuşmuyor")
    require(meta["tool_sha256"] == sha256(Path("tools/audit_legacy_alignment.py")), "Hizalama kodu uyuşmuyor")
    require(meta["replay_sha256"] == sha256(Path("replayman/replay.py")), "Replay kodu uyuşmuyor")
    require(meta["input_manifest_sha256"] == sha256(research / "dip-research/internal/input_manifest.csv"),
            "Eski hizalama girdi manifesti uyuşmuyor")
    for path, digest in meta["output_sha256"].items():
        require(sha256(output / path) == digest, f"Eski hizalama çıktısı uyuşmuyor: {path}")


def assert_summary(actual: pd.DataFrame, saved: pd.DataFrame) -> None:
    pd.testing.assert_frame_equal(actual.reset_index(drop=True), saved.reset_index(drop=True),
                                  check_dtype=False, check_exact=False, rtol=1e-9, atol=1e-12)


def independent_trade_bounds(bars: pd.DataFrame, start: int, end: int, atr: float) -> tuple[float, float]:
    """İlk temas/gap/sıra belirsizliği için doğrudan OHLC üzerinden örnek kontrol."""
    require(0 <= start <= end < len(bars), "İşlem penceresi geçersiz")
    entry = float(bars.open.iloc[start])
    stop, target = entry - atr, entry + 2 * atr
    require(entry > 0 and atr > 0 and stop > 0, "İşlem fiyatı/ATR geçersiz")
    for pos in range(start, end + 1):
        bar = bars.iloc[pos]
        if pos > start and (bar.open <= stop or bar.open >= target):
            value = float(bar.open) / entry - 1
            return value, value
        down, up = bar.low <= stop, bar.high >= target
        if down or up:
            low = stop if down else target
            high = target if up else stop
            return low / entry - 1, high / entry - 1
    final = float(bars.close.iloc[end]) / entry - 1
    return final, final


def independent_label(bars: pd.DataFrame, position: int, atr: float, references: pd.DataFrame, period: Period) -> str:
    """Kayıtlı referans pivotlardan dip etiketini satır formülüyle tekrar sınar."""
    if position + 7 >= len(bars) or bars.ts_utc.iloc[position + 7] >= period.end:
        return "censored"
    refs = references.loc[references.period == period.name]
    time_match = (refs.pivot_position - 2 <= position) & (position <= refs.pivot_position + 3)
    gap = float(bars.close.iloc[position]) - refs.pivot_low
    return "matched" if bool((time_match & (gap >= 0) & (gap <= atr)).any()) else "not_matched"


def verify_matching(output: Path, research: Path, markets: dict) -> dict:
    prior = pd.read_csv(output / "control_matches.csv")
    prior_pairs = pd.read_csv(output / "control_pairs.csv")
    assert_summary(summarize_controls(prior, prior_pairs), pd.read_csv(output / "control_summary.csv"))
    old = prior.loc[prior.control_status == "matched"].copy()
    require((old.bar_gap > 0).all(), "Geçmiş kontrol A'dan önce değil")
    require((pd.to_datetime(old.control_ts, utc=True) < pd.to_datetime(old.signal_ts, utc=True)).all(), "Önceki kontrol zamanı hatalı")
    require((week_starts(old.control_ts).to_numpy() == week_starts(old.signal_ts).to_numpy()).all(), "Önceki kontrol haftası farklı")
    require(not old.duplicated(["source", "asset_id", "interval", "control_position"]).any(), "Önceki kontrol tekrar kullanıldı")
    prior_ready = prior_pairs.loc[(prior_pairs.entry == "next_open") & prior_pairs.a_status.eq("observed")
                                  & prior_pairs.control_outcome_status.eq("observed")]
    begin, finish, later_a = (pd.to_datetime(prior_ready[c], utc=True)
                              for c in ("control_entry_ts", "control_end_ts", "signal_ts"))
    contains_future_a = int(((begin <= later_a) & (later_a <= finish)).sum())
    current = pd.read_csv(output / "contemporaneous_matches.csv")
    pairs = pd.read_csv(output / "contemporaneous_pairs.csv")
    assert_summary(summarize_contemporaneous(current, pairs), pd.read_csv(output / "contemporaneous_summary.csv"))
    match = current.loc[current.control_status == "matched"].copy()
    require((match.asset_id != match.control_asset_id).all(), "Eşzamanlı kontrol aynı hisse")
    require((match.trend_distance <= 1 + 1e-12).all() and match.volatility_ratio.between(.5, 2.).all(), "Eşzamanlı kontrol kaliperi hatalı")
    require(not match.duplicated(["source", "interval", "signal_ts", "control_asset_id"]).any(), "Eşzamanlı kontrol tekrar kullanıldı")
    require(not match.duplicated(["source", "signal_id"]).any() and not pairs.duplicated(["source", "signal_id", "entry"]).any(),
            "Sinyal veya çift kayıtları yineleniyor")
    expected = {(r.source, r.signal_id, entry) for r in match.itertuples() for entry in ("next_open", "delayed_open")}
    actual = set(pairs[["source", "signal_id", "entry"]].itertuples(index=False, name=None))
    require(actual == expected, "Her eş için iki benzersiz giriş kaydı yok")
    observed = pairs.a_status.eq("observed") & pairs.control_outcome_status.eq("observed")
    stamps = [pd.to_datetime(pairs[column], utc=True) for column in ("a_entry_ts", "control_entry_ts", "a_end_ts", "control_end_ts")]
    require(pd.concat(stamps, axis=1).loc[observed].notna().all().all(), "Gözlenmiş çiftin giriş veya bitiş zamanı eksik")
    equal = stamps[0].eq(stamps[1]) & stamps[2].eq(stamps[3])
    calculated = np.where(~observed, "censored_or_unknown", np.where(equal, "same", "different"))
    require((pairs.timing.to_numpy() == calculated).all(), "Çiftlerin zaman/sansür durumu hatalı")
    aligned = pairs.loc[pairs.timing == "same"]
    require((pd.to_datetime(aligned.a_entry_ts, utc=True) == pd.to_datetime(aligned.control_entry_ts, utc=True)).all(), "Girişler eşzamanlı değil")
    require((pd.to_datetime(aligned.a_end_ts, utc=True) == pd.to_datetime(aligned.control_end_ts, utc=True)).all(), "Bitişler eşzamanlı değil")
    manifests = {source: pd.read_csv(research / "dip-research" / source / "input_manifest.csv") for source in ("internal", "external")}
    references = {source: pd.read_csv(research / "dip-research" / source / "reference_pivots.csv") for source in ("internal", "external")}
    path_map = {(source, r.asset_id, r.interval): Path(r.path) for source, frame in manifests.items()
                for r in frame.itertuples() if r.kind != "benchmark"}
    reference_map = {(source, asset, interval): frame for source, refs in references.items()
                     for (asset, interval), frame in refs.groupby(["asset_id", "interval"], sort=False)}
    pair_index = pairs.set_index(["source", "signal_id", "entry"])
    match_index = match.set_index(["source", "signal_id"])
    bar_cache: dict[tuple, pd.DataFrame] = {}
    context_cache: dict[tuple, pd.DataFrame] = {}
    sample = match.sample(min(200, len(match)), random_state=123)
    label_checks = 0
    for row in sample.itertuples():
        keys = [(row.source, row.asset_id, row.interval), (row.source, row.control_asset_id, row.interval)]
        for key in keys:
            if key not in bar_cache:
                bar_cache[key] = load_external(path_map[key])[0] if row.source == "external" else load_bars(path_map[key])
                context_cache[key] = bar_context(bar_cache[key], key[1], key[2])
        a, b = (context_cache[keys[0]].iloc[int(row.signal_position)], context_cache[keys[1]].iloc[int(row.control_position)])
        require(a.ts_utc == b.ts_utc and pd.Timestamp(row.signal_ts) == a.ts_utc, "Farklı sinyal etiketleri")
        require(bool(a.raw_a) and bool(b.bullish) and not bool(b.raw_a), "Eşzamanlı bar niteliği uyuşmuyor")
        require(np.isclose(abs(a.prior_move_atr - b.prior_move_atr), row.trend_distance, atol=1e-10), "Eşleşme hareket farkı hatalı")
        require(np.isclose(a.prior_atr_fraction / b.prior_atr_fraction, row.volatility_ratio, atol=1e-10), "Eşleşme ATR oranı hatalı")
        require(np.isclose(a.atr, row.atr, atol=1e-10) and np.isclose(b.atr, row.control_atr, atol=1e-10), "Sinyal/kontrol ATR uyuşmuyor")
        period = period_at(a.ts_utc, EXTERNAL_PERIODS if row.source == "external" else INTERNAL_PERIODS)
        require(period is not None and period.name == row.period, "Eşleşme dönemi uyuşmuyor")
        pair = pair_index.loc[(row.source, row.signal_id, "next_open")]
        for key, context, label in ((keys[0], a, pair.a_label), (keys[1], b, pair.control_label)):
            ref = reference_map.get(key)
            if ref is None:
                ref = pd.DataFrame(columns=["period", "pivot_position", "pivot_low"])
            expected_label = independent_label(bar_cache[key], int(context.position), float(context.atr), ref, period)
            require(label == expected_label, "Sinyal/kontrol dip etiketi uyuşmuyor")
            label_checks += 1
    ready = aligned.sample(min(200, len(aligned)), random_state=512)
    price_checks = 0
    trade_checks = 0
    for row in ready.to_dict("records"):
        for prefix, asset in (("a", row["asset_id"]), ("control", row["control_asset_id"])):
            key = (row["source"], asset, row["interval"])
            if key not in bar_cache:
                bar_cache[key] = load_external(path_map[key])[0] if row["source"] == "external" else load_bars(path_map[key])
            bars = bar_cache[key]
            pos = int(row["signal_position"] if prefix == "a" else row["control_position"])
            start = pos + (1 if row["entry"] == "next_open" else 2)
            end = start + 19
            require(pd.Timestamp(row[f"{prefix}_entry_ts"]) == bars.ts_utc.iloc[start] and
                    pd.Timestamp(row[f"{prefix}_end_ts"]) == bars.ts_utc.iloc[end], "Eşzamanlı sonuç pozisyonu hatalı")
            raw = float(bars.close.iloc[end]) / float(bars.open.iloc[start]) - 1
            require(np.isclose(row[f"{prefix}_fixed_return"], raw, rtol=1e-9, atol=1e-10), "Eşzamanlı sonuç fiyatı hatalı")
            record = match_index.loc[(row["source"], row["signal_id"])]
            atr = float(record.atr if prefix == "a" else record.control_atr)
            lower, upper = independent_trade_bounds(bars, start, end, atr)
            require(np.isclose(row[f"{prefix}_trade_lower"], lower, rtol=1e-9, atol=1e-10) and
                    np.isclose(row[f"{prefix}_trade_upper"], upper, rtol=1e-9, atol=1e-10), "İşlem alt/üst aritmetiği uyuşmuyor")
            trade_checks += 1
            if row["source"] == "internal":
                market = markets[row["interval"]]
                first, last = bars.ts_utc.iloc[start], bars.ts_utc.iloc[end]
                if first in market.index and last in market.index:
                    bench = float(market.at[last, "close"]) / float(market.at[first, "open"]) - 1
                    require(np.isclose(row[f"{prefix}_excess_return"], raw - bench, atol=1e-10), "Eşzamanlı XU100 farkı hatalı")
                else:
                    require(pd.isna(row[f"{prefix}_excess_return"]), "Eksik endeks sayılmış")
            else:
                require(pd.isna(row[f"{prefix}_excess_return"]), "Harici bilinmeyen endeks doldurulmuş")
            price_checks += 1
    return {"prior_a": len(prior), "prior_pairs": len(old), "prior_next_open_observed": len(prior_ready),
            "prior_control_windows_containing_the_later_a": contains_future_a,
            "same_time_a": len(current), "same_time_pairs": len(match),
            "matching_sample_checked": len(sample), "sampled_label_checks": label_checks,
            "aligned_event_pairs_sampled": len(ready), "sampled_price_checks": price_checks,
            "sampled_trade_bound_checks": trade_checks}


def verify_p6(output: Path, research: Path, markets: dict) -> dict:
    data = pd.read_csv(output / "p6_same_end_pairs.csv")
    assert_summary(summarize_p6(data), pd.read_csv(output / "p6_same_end_summary.csv"))
    manifest = pd.read_csv(research / "p6-causal/input_manifest.csv")
    paths = {(r.asset_id, r.interval): Path(r.path) for r in manifest.itertuples() if r.kind == "internal_equity"}
    cache = {}
    sample = data.sample(min(200, len(data)), random_state=73)
    for r in sample.itertuples():
        key = (r.asset_id, r.interval)
        if key not in cache:
            cache[key] = load_bars(paths[key])
        bars = cache[key]
        f, c = int(r.failure_position), int(r.confirmation_position)
        end, entry = f + 20, c + 1
        require(end >= entry and pd.Timestamp(r.common_end_ts) == bars.ts_utc.iloc[end], "P6 ortak bitiş hatalı")
        require(pd.Timestamp(r.confirmation_entry_ts) == bars.ts_utc.iloc[entry], "P6 teyit sonrası giriş hatalı")
        one = r.thesis_sign * (float(bars.close.iloc[end]) / float(bars.close.iloc[f]) - 1)
        two = r.thesis_sign * (float(bars.close.iloc[end]) / float(bars.open.iloc[entry]) - 1)
        require(np.isclose(one, r.oracle_return, atol=1e-10) and np.isclose(two, r.confirmation_return, atol=1e-10), "P6 aynı-bitiş aritmetiği hatalı")
        require(r.remaining_bars == end - entry + 1, "P6 elde tutma bar sayısı hatalı")
        market = markets[r.interval]
        first, later, last = bars.ts_utc.iloc[f], bars.ts_utc.iloc[entry], bars.ts_utc.iloc[end]
        if all(ts in market.index for ts in (first, later, last)):
            exit_price = float(market.at[last, "close"])
            oracle_market = exit_price / float(market.at[first, "close"]) - 1
            confirm_market = exit_price / float(market.at[later, "open"]) - 1
            require(np.isclose(r.oracle_excess, one - r.thesis_sign * oracle_market, atol=1e-10) and
                    np.isclose(r.confirmation_excess, two - r.thesis_sign * confirm_market, atol=1e-10),
                    "P6 ortak-bitiş XU100 aritmetiği hatalı")
        else:
            require(pd.isna(r.oracle_excess) and pd.isna(r.confirmation_excess), "Eksik P6 endeksi doldurulmuş")
    return {"same_end_events": len(data), "sample_checked": len(sample)}


def verify_acceptance(output: Path, research: Path, markets: dict) -> dict:
    events = pd.read_csv(output / "acceptance_events.csv")
    inventory = pd.read_csv(output / "acceptance_inventory.csv")
    assert_summary(summarize_acceptance(events, inventory), pd.read_csv(output / "acceptance_summary.csv"))
    require(not events.duplicated(["asset_id", "tie_break", "signal_position"]).any(), "Acceptance hisse/bar tekilleştirmesi hatalı")
    require((inventory.raw_level_events >= inventory.unique_bar_events).all(), "Ham acceptance sayısı tekilden küçük")
    inventory_keys = ["asset_id", "interval", "tie_break", "period"]
    require(not inventory.duplicated(inventory_keys).any(), "Acceptance envanter anahtarı yinelenmiş")
    inventory_index = inventory.set_index(inventory_keys)
    event_counts = events.groupby(inventory_keys).size()
    require(event_counts.index.isin(inventory_index.index).all(), "Acceptance olayı envanterde yok")
    expected_counts = event_counts.reindex(inventory_index.index, fill_value=0)
    require((expected_counts.to_numpy() == inventory_index.unique_bar_events.to_numpy()).all(), "Envanter ve tekil olay sayıları uyuşmuyor")
    manifest = pd.read_csv(research / "dip-research/internal/input_manifest.csv")
    paths = {(r.asset_id, r.interval): Path(r.path) for r in manifest.itertuples() if r.kind == "internal_equity"}
    cache = {}
    sample = events.sample(min(200, len(events)), random_state=31)
    arithmetic_checks = 0
    for r in sample.to_dict("records"):
        key = (r["asset_id"], r["interval"])
        if key not in cache:
            cache[key] = load_bars(paths[key])
        bars, market = cache[key], markets[r["interval"]]
        signal = int(r["signal_position"])
        p = period_at(bars.ts_utc.iloc[signal], INTERNAL_PERIODS)
        require(p is not None and p.name == r["period"] and pd.Timestamp(r["signal_ts"]) == bars.ts_utc.iloc[signal],
                "Acceptance sinyal/dönem uyuşmuyor")
        require(int(r["source_confirmed_position"]) < signal, "Acceptance pivot teyidi öncesinde")
        for entry, lag in (("next_open", 1), ("delayed_open", 2)):
            if r[f"{entry}__status"] != "observed":
                continue
            start, end = signal + lag, signal + lag + 59
            require(end < len(bars) and bars.ts_utc.iloc[end] < p.end, "Acceptance ufku bölüm dışına taşıyor")
            require(pd.Timestamp(r[f"{entry}__start_ts"]) == bars.ts_utc.iloc[start] and
                    pd.Timestamp(r[f"{entry}__end_ts"]) == bars.ts_utc.iloc[end], "Acceptance giriş/bitiş etiketi hatalı")
            ret = -(float(bars.close.iloc[end]) / float(bars.open.iloc[start]) - 1)
            require(np.isclose(ret, r[f"{entry}__directional_return"], atol=1e-10), "Acceptance yönlü getiri hatalı")
            first, last = bars.ts_utc.iloc[start], bars.ts_utc.iloc[end]
            if first in market.index and last in market.index:
                bench = float(market.at[last, "close"]) / float(market.at[first, "open"]) - 1
                require(np.isclose(ret + bench, r[f"{entry}__directional_excess"], atol=1e-10), "Acceptance XU100 farkı hatalı")
            else:
                require(pd.isna(r[f"{entry}__directional_excess"]), "Acceptance eksik endeksi doldurulmuş")
            arithmetic_checks += 1
    assets = np.random.default_rng(610).choice(sorted(inventory.asset_id.unique()),
                                               size=min(10, inventory.asset_id.nunique()), replace=False)
    replayed = 0
    for asset in assets:
        key = (asset, "4h")
        if key not in cache:
            cache[key] = load_bars(paths[key])
        bars = cache[key]
        features = causal_features(bars)
        for tie in ("leftmost", "rightmost"):
            swings = confirmed_swings(bars, features, config=SwingConfig(2, 2, tie_break=tie), level="minor")
            raw, unique = down_acceptance_representatives(structure_events(bars, features, swings))
            for period in INTERNAL_PERIODS:
                raw_part = raw.loc[raw.event_position.map(lambda p: period_at(bars.ts_utc.iloc[int(p)], [period]) is not None)]
                part = unique.loc[unique.event_position.map(lambda p: period_at(bars.ts_utc.iloc[int(p)], [period]) is not None)]
                stored = events.loc[(events.asset_id == asset) & (events.tie_break == tie) & (events.period == period.name)]
                recorded = inventory_index.loc[(asset, "4h", tie, period.name)]
                require(len(raw_part) == recorded.raw_level_events and len(part) == recorded.unique_bar_events,
                        "Acceptance olay envanteri yeniden üretilemedi")
                expected = sorted((int(x.event_position), int(x.source_pivot_position), int(x.source_confirmed_position))
                                  for x in part.itertuples())
                actual = sorted((int(x.signal_position), int(x.source_pivot_position), int(x.source_confirmed_position))
                                for x in stored.itertuples())
                require(expected == actual, "Tekil acceptance temsilcileri yeniden üretilemedi")
        replayed += 1
    return {"events": len(events), "sampled_events": len(sample), "sampled_entry_arithmetic": arithmetic_checks,
            "sampled_assets_replayed_for_both_tie_rules": replayed}


def verify_external(output: Path, research: Path) -> dict:
    annual, assets, weeks, overall = external_stability(research / "dip-research")
    weeks["week"] = weeks.week.astype(str)
    for name, frame in (("external_annual.csv", annual), ("external_assets.csv", assets), ("external_weeks.csv", weeks)):
        assert_summary(frame, pd.read_csv(output / name))
    saved = json.loads((output / "external_stability.json").read_text(encoding="utf-8"))

    def compare(left, right) -> None:
        if isinstance(left, dict):
            require(isinstance(right, dict) and left.keys() == right.keys(), "Harici özet anahtarları uyuşmuyor")
            for key in left:
                compare(left[key], right[key])
        elif isinstance(left, (float, int)):
            require(isinstance(right, (float, int)) and np.isclose(left, right, rtol=1e-9, atol=1e-12),
                    "Harici özet sayı uyuşmuyor")
        else:
            require(left == right, "Harici özet uyuşmuyor")

    compare(overall, saved)
    return {"observed_events": overall["events"], "assets": overall["assets"], "observed_weeks": overall["weeks"]}


def verify_alignment(output: Path, research: Path, markets: dict) -> dict:
    data = pd.read_csv(output / "legacy_alignment_assets.csv")
    saved = pd.read_csv(output / "legacy_alignment_summary.csv")
    grouped = data.groupby(["interval", "horizon"], as_index=False).agg(
        assets=("asset_id", "nunique"), stock_windows=("stock_windows", "sum"), old_comparable=("old_comparable", "sum"),
        old_end_mismatches=("old_end_mismatches", "sum"), start_missing=("start_missing", "sum"),
        old_end_unavailable=("old_end_unavailable", "sum"), exact_end_missing=("exact_end_missing", "sum"))
    grouped["mismatch_fraction"] = grouped.old_end_mismatches / grouped.old_comparable.replace(0, np.nan)
    assert_summary(grouped, saved)
    manifest = pd.read_csv(research / "dip-research/internal/input_manifest.csv")
    paths = {(r.asset_id, r.interval): Path(r.path) for r in manifest.itertuples() if r.kind == "internal_equity"}
    sample = data.sample(min(20, len(data)), random_state=19)
    for row in sample.to_dict("records"):
        stock = load_bars(paths[(row["asset_id"], row["interval"])])
        check = window_alignment(stock, markets[row["interval"]], int(row["horizon"]))
        require(all(row[k] == v for k, v in check.items()), "Eski endeks kaydırması sayımı uyuşmuyor")
    return {"stock_windows": int(saved.stock_windows.sum()), "old_mismatches": int(saved.old_end_mismatches.sum()),
            "sampled_asset_horizon_rows": len(sample)}


def audit(root: Path, research: Path, output: Path) -> dict:
    verify_metadata(output, research)
    verified = {s: verify_hashes(research / "dip-research" / s) for s in ("internal", "external")}
    verified["p6"] = verify_hashes(research / "p6-causal")
    markets = verified_markets(root, research / "dip-research/internal")
    return {"audited_at_utc": datetime.now(timezone.utc).isoformat(), "status": "passed",
            "audit_tool_sha256": sha256(Path(__file__)), "source_files_verified": verified,
            "matching": verify_matching(output, research, markets), "p6": verify_p6(output, research, markets),
            "acceptance": verify_acceptance(output, research, markets), "external": verify_external(output, research),
            "legacy_alignment": verify_alignment(output, research, markets),
            "scope": "Artifact integrity and selected arithmetic, not independent source, causal advantage or actual execution."}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path("data/ohlcv"))
    p.add_argument("--research", type=Path, default=Path("research/measurements"))
    p.add_argument("--output", type=Path, default=Path("research/measurements/general-review"))
    args = p.parse_args()
    result = audit(args.root, args.research, args.output)
    (args.output / "AUDIT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
