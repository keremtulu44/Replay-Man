"""Gerçek yfinance kod yolu, sahte HTTP yanıtları: internete çıkmaz."""
import json
from urllib.parse import urlparse

import pandas as pd
import pytest
import requests
import yfinance as yf
from yfinance.data import SingletonMeta, YfData

from replayman.catalog import Asset
from replayman.errors import AccessDenied, RateLimited
from replayman.provider import PoliteSession, YahooProvider


@pytest.fixture
def isolated_yfinance(tmp_path, monkeypatch):
    monkeypatch.setattr(SingletonMeta, "_instances", {})
    yf.set_tz_cache_location(str(tmp_path / "yf-cache"))
    # Önceki çalışmalardan alınan cookie'ler bu testi etkilemesin.
    monkeypatch.setattr(YfData, "_load_cookie_curlCffi", lambda self: False)
    monkeypatch.setattr(YfData, "_save_cookie_curlCffi", lambda self: False)


def response(status, body, url, content_type="application/json"):
    result = requests.Response()
    result.status_code = status
    result.url = url
    result._content = body.encode()
    result.headers["Content-Type"] = content_type
    return result


def test_real_yfinance_path_cookie_404_and_chart_success(settings, isolated_yfinance, monkeypatch):
    calls = []
    timestamp = int(pd.Timestamp("2026-01-01", tz="UTC").timestamp())
    data = {"chart": {"error": None, "result": [{
        "meta": {"currency": "TRY", "symbol": "TESTFAKE.IS", "instrumentType": "EQUITY",
                 "exchangeTimezoneName": "UTC", "gmtoffset": 0, "timezone": "UTC",
                 "regularMarketTime": timestamp, "validRanges": ["1d"], "dataGranularity": "1d"},
        "timestamp": [timestamp],
        "indicators": {"quote": [{"open": [10], "high": [11], "low": [9], "close": [10.5], "volume": [100]}],
                       "adjclose": [{"adjclose": [10.5]}]},
    }]}}

    def fake_request(self, method, url, *args, **kwargs):
        calls.append((url, kwargs.get("timeout")))
        host = urlparse(url).hostname
        if host == "fc.yahoo.com":
            return response(404, "", url)
        if urlparse(url).path == "/v1/test/getcrumb":
            return response(200, "crumb", url, "text/plain")
        assert "/v8/finance/chart/TESTFAKE.IS" in url
        return response(200, json.dumps(data), url)

    monkeypatch.setattr(requests.Session, "request", fake_request)
    provider = YahooProvider(
        settings.with_overrides(request_timeout_seconds=15),
        session=PoliteSession(timeout=15),
    )
    asset = Asset("TEST", "bist100_equity", "Test", "TESTFAKE", "TESTFAKE.IS", "equity", "TRY", "true")
    gated = []
    try:
        result = provider.fetch(asset, "1d", pd.Timestamp("2026-01-01", tz="UTC"),
                                pd.Timestamp("2026-01-02", tz="UTC"), before_request=lambda: gated.append(1))
    finally:
        provider.close()
    assert len(result.frame) == 1
    assert result.frame.iloc[0]["Close"] == 10.5
    assert result.metadata["currency"] == "TRY"
    assert len(gated) == len(calls) >= 2
    assert all(timeout <= 15 for _, timeout in calls)


@pytest.mark.parametrize("status, error", [(403, AccessDenied), (429, RateLimited)])
def test_real_yfinance_path_stops_at_first_block(settings, isolated_yfinance, monkeypatch, status, error):
    calls = []

    def fake_request(self, method, url, *args, **kwargs):
        calls.append(url)
        return response(status, "blocked", url)

    monkeypatch.setattr(requests.Session, "request", fake_request)
    provider = YahooProvider(settings, session=PoliteSession(timeout=settings.request_timeout_seconds))
    asset = Asset("TEST", "bist100_equity", "Test", "BLOCKTEST", "BLOCKTEST.IS", "equity", "TRY", "true")
    try:
        with pytest.raises(error):
            provider.fetch(asset, "1d", pd.Timestamp("2026-01-01", tz="UTC"),
                           pd.Timestamp("2026-01-02", tz="UTC"), before_request=lambda: None)
    finally:
        provider.close()
    assert len(calls) == 1
