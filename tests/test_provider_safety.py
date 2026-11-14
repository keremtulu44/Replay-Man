import pytest
import requests

from replayman.errors import AccessDenied, PermanentHTTP, RateLimited, TransientHTTP
from replayman.provider import PoliteSession, _retry_after_seconds


class Response:
    def __init__(self, status, headers=None, text=""):
        self.status_code = status
        self.headers = headers or {}
        self.text = text


def test_polite_session_gates_and_blocks(monkeypatch):
    calls = []

    def fake_request(self, method, url, *args, **kwargs):
        return Response(429, {"Retry-After": "12"})

    monkeypatch.setattr(requests.Session, "request", fake_request)
    session = PoliteSession()
    session.before_request = lambda: calls.append(1)
    with pytest.raises(RateLimited) as exc:
        session.get("https://example.invalid")
    assert calls == [1]
    assert exc.value.retry_after == 12


@pytest.mark.parametrize("status,cls", [(403, AccessDenied), (503, TransientHTTP), (404, PermanentHTTP)])
def test_polite_session_status_mapping(monkeypatch, status, cls):
    monkeypatch.setattr(requests.Session, "request", lambda self, *a, **k: Response(status))
    with pytest.raises(cls):
        PoliteSession().get("https://example.invalid")


def test_retry_after_parser():
    assert _retry_after_seconds("30") == 30
    assert _retry_after_seconds(None) is None


def test_yahoo_cookie_404_is_allowed_but_chart_404_is_not(monkeypatch):
    monkeypatch.setattr(requests.Session, "request", lambda self, *a, **k: Response(404))
    session = PoliteSession()
    assert session.get("https://fc.yahoo.com/").status_code == 404
    with pytest.raises(PermanentHTTP):
        session.get("https://query1.finance.yahoo.com/v8/finance/chart/INVALID")
    with pytest.raises(PermanentHTTP):
        session.get("https://fc.yahoo.com.evil.example/")


def test_timeout_is_capped_for_yfinance_internal_requests(monkeypatch):
    timeouts = []

    def fake_request(self, method, url, *args, **kwargs):
        timeouts.append(kwargs.get("timeout"))
        return Response(200)

    monkeypatch.setattr(requests.Session, "request", fake_request)
    session = PoliteSession(timeout=15)
    session.get("https://example.invalid", timeout=30)
    session.get("https://example.invalid", timeout=5)
    session.get("https://example.invalid")
    assert timeouts == [15, 5, 15]
