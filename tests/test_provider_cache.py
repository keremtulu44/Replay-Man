import pandas as pd

from replayman.catalog import Asset
from replayman.provider import YahooProvider


def test_provider_disk_cache_roundtrip(settings):
    provider = YahooProvider(settings)
    asset = Asset("BIST_ASELS", "bist100_equity", "Aselsan", "ASELS", "ASELS.IS", "equity", "TRY", "true")
    start = pd.Timestamp("2026-01-01", tz="UTC")
    end = pd.Timestamp("2026-01-02", tz="UTC")
    frame = pd.DataFrame({"Open": [1], "High": [2], "Low": [0.5], "Close": [1.5]}, index=pd.date_range(start, periods=1, freq="h"))
    key = provider.cache_key(asset, "1h", start, end)
    provider._save_cache(key, frame, {"currency": "TRY"})
    loaded = provider._load_cache(key)
    assert loaded is not None
    pd.testing.assert_frame_equal(loaded[0], frame)
    assert loaded[1]["currency"] == "TRY"
    provider.close()
