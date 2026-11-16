from pathlib import Path

import pytest

from replayman.catalog import load_catalog
from replayman.config import Settings


def test_real_catalog_has_125_enabled_assets():
    root = Path(__file__).resolve().parents[1]
    assets, digest = load_catalog(root / "data/universe.csv")
    assert len(assets) == 125
    assert len({a.yahoo_symbol for a in assets}) == 125
    assert digest


def test_catalog_filter_and_disabled(catalog_path):
    assets, _ = load_catalog(catalog_path)
    assert [a.local_symbol for a in assets] == ["ASELS", "XU100", "GOLD"]
    assets, _ = load_catalog(catalog_path, symbols=["gc=f"])
    assert assets[0].id == "METAL_GOLD"
    with pytest.raises(ValueError):
        load_catalog(catalog_path, symbols=["YOK"])


def test_settings_reject_unknown(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text('{"proxy_rotation": true}', encoding="utf-8")
    with pytest.raises(ValueError, match="Bilinmeyen"):
        Settings.load(path, base_dir=tmp_path)


def test_settings_reject_bad_intervals(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text('{"intervals": ["1m"]}', encoding="utf-8")
    with pytest.raises(ValueError):
        Settings.load(path, base_dir=tmp_path)
