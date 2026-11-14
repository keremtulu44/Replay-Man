"""Yahoo/yfinance sağlayıcısı. Ekstra bot-aşımı, proxy veya CAPTCHA çözümü yoktur."""
from __future__ import annotations

import hashlib
import json
import logging
import pickle
import tempfile
from dataclasses import dataclass
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Callable
from urllib.parse import urlparse

import pandas as pd
import requests

from .catalog import Asset
from .config import Settings
from .errors import AccessDenied, InvalidData, NoData, PermanentHTTP, RateLimited, TransientHTTP

logger = logging.getLogger(__name__)


def _retry_after_seconds(header: str | None) -> float | None:
    if not header:
        return None
    try:
        return max(0.0, float(header))
    except ValueError:
        try:
            when = parsedate_to_datetime(header)
            import time
            return max(0.0, when.timestamp() - time.time())
        except Exception:
            return None


class PoliteSession(requests.Session):
    """requests oturumu; varsayılan Python user-agent korunur, kimlik taklidi eklenmez."""

    def __init__(self, timeout: float | None = None) -> None:
        super().__init__()
        self.timeout = timeout
        self.before_request: Callable[[], None] | None = None

    def request(self, method, url, *args, **kwargs):
        if self.before_request is not None:
            self.before_request()
        if self.timeout is not None:
            timeout = kwargs.get("timeout")
            if timeout is None or (isinstance(timeout, (int, float)) and timeout > self.timeout):
                kwargs["timeout"] = self.timeout
        response = super().request(method, url, *args, **kwargs)
        status = response.status_code
        if status in (401, 403):
            raise AccessDenied(status, f"HTTP {status}: Yahoo erişimi reddetti; istekler durdurulacak")
        if status == 429:
            raise RateLimited(retry_after=_retry_after_seconds(response.headers.get("Retry-After")))
        if 500 <= status < 600:
            raise TransientHTTP(status)
        # Yahoo çerez başlangıç adresi 404 ile de geçerli cookie döndürebilir.
        # yfinance bu yanıtı okur; veri endpointlerindeki 404 hâlâ hatadır.
        cookie_404 = status == 404 and urlparse(url).hostname == "fc.yahoo.com"
        if status >= 400 and not cookie_404:
            raise PermanentHTTP(status, f"HTTP {status}: {response.text[:200]}")
        return response


@dataclass
class FetchResult:
    frame: pd.DataFrame
    from_cache: bool
    metadata: dict
    cache_key: str


class YahooProvider:
    def __init__(self, settings: Settings, session: requests.Session | None = None) -> None:
        import yfinance as yf

        self.settings = settings
        self.yf = yf
        yf.config.debug.hide_exceptions = False
        yf.config.network.retries = 0
        yf.config.network.proxy = None
        self.session = session or PoliteSession(settings.request_timeout_seconds)
        self.cache_dir = Path(settings.cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def close(self) -> None:
        self.session.close()

    def cache_key(self, asset: Asset, interval: str, start: pd.Timestamp, end: pd.Timestamp) -> str:
        payload = {
            "provider": "yahoo-yfinance",
            "yfinance": self.yf.__version__,
            "symbol": asset.yahoo_symbol,
            "interval": interval,
            "start": start.isoformat(),
            "end": end.isoformat(),
            "auto_adjust": self.settings.auto_adjust,
            "back_adjust": self.settings.back_adjust,
            "repair": self.settings.repair,
            "keepna": self.settings.keepna,
            "actions": self.settings.actions,
            "prepost": self.settings.prepost,
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    def _cache_paths(self, key: str) -> tuple[Path, Path]:
        return self.cache_dir / f"{key}.pkl", self.cache_dir / f"{key}.json"

    def _load_cache(self, key: str) -> tuple[pd.DataFrame, dict] | None:
        data_path, meta_path = self._cache_paths(key)
        if not data_path.exists() or not meta_path.exists():
            return None
        try:
            with data_path.open("rb") as handle:
                frame = pickle.load(handle)
            metadata = json.loads(meta_path.read_text(encoding="utf-8"))
            if not isinstance(frame, pd.DataFrame):
                raise InvalidData("Önbellek DataFrame değil")
            return frame, metadata
        except Exception as exc:
            logger.warning("Önbellek okunamadı (%s); ağdan denenecek: %s", key[:12], exc)
            return None

    def _save_cache(self, key: str, frame: pd.DataFrame, metadata: dict) -> None:
        data_path, meta_path = self._cache_paths(key)
        with tempfile.NamedTemporaryFile(dir=self.cache_dir, delete=False, suffix=".tmp") as handle:
            tmp = Path(handle.name)
        try:
            with tmp.open("wb") as handle:
                pickle.dump(frame, handle, protocol=pickle.HIGHEST_PROTOCOL)
            tmp.replace(data_path)
            meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        finally:
            tmp.unlink(missing_ok=True)

    def fetch(
        self,
        asset: Asset,
        interval: str,
        start: pd.Timestamp,
        end: pd.Timestamp,
        before_request: Callable[[], None] | None = None,
    ) -> FetchResult:
        key = self.cache_key(asset, interval, start, end)
        cached = self._load_cache(key)
        if cached is not None:
            frame, metadata = cached
            return FetchResult(frame, True, metadata, key)

        if isinstance(self.session, PoliteSession):
            self.session.before_request = before_request
        ticker = self.yf.Ticker(asset.yahoo_symbol, session=self.session)
        frame = ticker.history(
            start=start.to_pydatetime(),
            end=end.to_pydatetime(),
            interval=interval,
            auto_adjust=self.settings.auto_adjust,
            back_adjust=self.settings.back_adjust,
            actions=self.settings.actions,
            prepost=self.settings.prepost,
            repair=self.settings.repair,
            keepna=self.settings.keepna,
            rounding=False,
            timeout=self.settings.request_timeout_seconds,
        )
        if frame is None or frame.empty:
            raise NoData(f"{asset.yahoo_symbol} {interval} {start.date()}->{end.date()}: boş yanıt")
        # HistoryMetadata bir lazy Mapping: dict(...) ek intraday isteği yapar ve
        # Timestamp/DataFrame değerleri JSON önbelleğini bozabilir. Yalnızca
        # normalizasyonun ihtiyaç duyduğu, scalar alanları al.
        history_metadata = ticker.history_metadata
        metadata = {}
        if history_metadata is not None:
            for field in ("symbol", "currency", "instrumentType", "exchangeTimezoneName"):
                value = history_metadata.get(field)
                if value is not None:
                    metadata[field] = str(value)
        metadata.setdefault("fetchedAt", pd.Timestamp.now(tz='UTC').isoformat())
        self._save_cache(key, frame, metadata)
        return FetchResult(frame, False, metadata, key)
