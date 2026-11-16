"""Hata sınıflandırma. Engelleme/aşım değil, durma ve yeniden deneme politikası."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FetchFailure(Exception):
    kind: str
    message: str
    status: int | None = None
    retry_after: float | None = None

    def __str__(self) -> str:
        return self.message


class AccessDenied(FetchFailure):
    def __init__(self, status: int, message: str = "") -> None:
        super().__init__("access_denied", message or f"HTTP {status}: erişim reddedildi", status)


class RateLimited(FetchFailure):
    def __init__(self, message: str = "HTTP 429: hız sınırı", retry_after: float | None = None, status: int | None = 429) -> None:
        super().__init__("rate_limit", message, status, retry_after)


class TransientHTTP(FetchFailure):
    def __init__(self, status: int, message: str = "") -> None:
        super().__init__("transient", message or f"HTTP {status}: geçici sunucu hatası", status)


class PermanentHTTP(FetchFailure):
    def __init__(self, status: int, message: str = "") -> None:
        super().__init__("permanent", message or f"HTTP {status}: kalıcı istemci hatası", status)


class NoData(FetchFailure):
    def __init__(self, message: str = "Yahoo bu aralıkta veri döndürmedi") -> None:
        super().__init__("no_data", message)


class InvalidData(FetchFailure):
    def __init__(self, message: str) -> None:
        super().__init__("invalid_data", message)


class RunLimitReached(Exception):
    """Bu çalıştırmadaki ağ isteği bütçesi doldu."""


RETRYABLE_KINDS = {"transient", "rate_limit", "unknown"}
PERMANENT_KINDS = {"access_denied", "permanent", "no_data", "invalid_data"}


def classify_error(exc: BaseException) -> FetchFailure:
    if isinstance(exc, FetchFailure):
        return exc
    try:
        from yfinance.exceptions import (
            YFInvalidPeriodError,
            YFPricesMissingError,
            YFRateLimitError,
            YFTickerMissingError,
            YFTzMissingError,
        )
    except ImportError:  # test/çevrimdışı ortam
        YFInvalidPeriodError = YFPricesMissingError = YFRateLimitError = ()
        YFTickerMissingError = YFTzMissingError = ()
    if isinstance(exc, YFRateLimitError):
        # yfinance 429 görmeden de "Too Many Requests" içerikli yanıt için
        # bu hatayı verebilir; doğrudan HTTP 429 diye raporlamayalım.
        return RateLimited(f"yfinance hız sınırı bildirdi (HTTP kodu doğrulanmadı): {exc}", status=None)
    if isinstance(exc, YFPricesMissingError):
        message = str(exc)
        lower = message.lower()
        if "requested range" in lower or "invalid interval" in lower or "data not available" in lower:
            return FetchFailure("permanent", message)
        return NoData(message)
    if isinstance(exc, (YFTickerMissingError, YFTzMissingError, YFInvalidPeriodError)):
        return FetchFailure("permanent", str(exc))
    try:
        import requests
        if isinstance(exc, (requests.Timeout, requests.ConnectionError)):
            return FetchFailure("transient", f"{type(exc).__name__}: {exc}")
    except ImportError:
        pass
    if isinstance(exc, (TimeoutError, ConnectionError)):
        return FetchFailure("transient", f"{type(exc).__name__}: {exc}")
    if isinstance(exc, ValueError) and "json" in str(exc).lower():
        return FetchFailure("transient", str(exc))
    return FetchFailure("unknown", f"{type(exc).__name__}: {exc}")
