import pandas as pd
import pytest

from replayman.catalog import Asset
from replayman.errors import InvalidData
from replayman.normalize import merge_save_prices, normalize_prices
from replayman.resample import derive_timeframes


def asset(category="bist100_equity", symbol="ASELS.IS"):
    return Asset("BIST_ASELS", category, "Aselsan", "ASELS", symbol, "equity", "TRY", "true")


def raw_frame():
    idx = pd.date_range("2026-01-05 10:00", periods=3, freq="h", tz="Europe/Istanbul").tz_convert("UTC")
    return pd.DataFrame(
        {"Open": [10, 11, 12], "High": [11, 12, 13], "Low": [9, 10, 11], "Close": [10.5, 11.5, 12.5], "Volume": [100, 200, 300]},
        index=idx,
    )


def test_normalize_and_merge_dedup(tmp_path, settings):
    df, stats = normalize_prices(raw_frame(), asset(), "1h", "now", settings=settings, series_id="series-test")
    assert len(df) == 3
    assert stats["dropped_invalid"] == 0
    path = tmp_path / "prices.csv"
    assert merge_save_prices(path, df) == 3
    assert merge_save_prices(path, df.iloc[-1:]) == 3


def test_normalize_drops_invalid_ohlc(settings):
    frame = raw_frame()
    frame.iloc[0, frame.columns.get_loc("High")] = 1
    df, stats = normalize_prices(frame, asset(), "1h", "now", settings=settings, series_id="series-test")
    assert len(df) == 2
    assert stats["dropped_invalid"] == 1


def test_normalize_rejects_missing_columns(settings):
    with pytest.raises(InvalidData):
        normalize_prices(pd.DataFrame({"Close": [1]}), asset(), "1h", "now", settings=settings, series_id="series-test")


def test_bist_session_derive_complete_flags():
    local = pd.to_datetime(
        ["2026-01-05 10:00", "2026-01-05 11:00", "2026-01-05 12:00", "2026-01-05 14:00", "2026-01-05 15:00", "2026-01-05 16:00", "2026-01-05 17:00"]
    ).tz_localize("Europe/Istanbul")
    frame = pd.DataFrame(
        {"open": 10, "high": 11, "low": 9, "close": 10.5, "adj_close": 10.5, "volume": 100, "dividends": 0, "stock_splits": 0, "capital_gains": 0},
        index=local.tz_convert("UTC"),
    )
    frame["ts_utc"] = frame.index.strftime("%Y-%m-%dT%H:%M:%SZ")
    frame = frame.reset_index(drop=True)
    derived = derive_timeframes(frame, asset(), series_id="series-test")
    assert set(derived) == {"2h", "4h", "1d_from_1h"}
    daily = derived["1d_from_1h"].iloc[0]
    assert daily["bar_count"] == 7
    assert bool(daily["complete"])
    assert daily["volume"] == 700
    assert all((frame["series_id"] == "series-test").all() for frame in derived.values())
    two = derived["2h"]
    assert len(two) == 4
    assert bool(two.iloc[1]["complete"])
    four = derived["4h"]
    assert len(four) == 2
    assert four.iloc[0]["bar_count"] == 3
    assert four.iloc[1]["bar_count"] == 4


def test_non_bist_derive_uses_utc(settings):
    df, _ = normalize_prices(raw_frame(), asset("metals", "GC=F"), "1h", "now", settings=settings, series_id="series-test")
    derived = derive_timeframes(df, asset("metals", "GC=F"), series_id="series-test")
    assert "2h" in derived
    assert derived["2h"].iloc[0]["derived_from"] == "1h"
