"""
Dataクラスの定義
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import NamedTuple


class XY(NamedTuple):
    """2次元座標を格納するクラス"""

    x: float | Decimal
    y: float | Decimal


class XYZ(NamedTuple):
    """3次元座標を格納するクラス"""

    x: float
    y: float
    z: float


class Bounds(NamedTuple):
    """
    ## Summary:
        バウンディングボックスを表すクラス
    Args:
        x_min (float):
            x軸の最小値（経度）
        y_min (float):
            y軸の最小値（緯度）
        x_max (float):
            x軸の最大値（経度）
        y_max (float):
            y軸の最大値（緯度）
    """

    x_min: float
    y_min: float
    x_max: float
    y_max: float


@dataclass
class MeshDesignJP(object):
    """
    ## Summary:
        日本で使用される、地域メッシュを作成する為のクラス
    Args:
        lon(float):
            経度（10進数）
        lat(float):
            緯度（10進数）
    """

    lon: float
    lat: float

    def __post_init__(self):
        if not (-180.0 <= self.lon <= 180.0):
            raise ValueError("経度は-180.0から180.0の範囲で指定してください。")
        if not (-90.0 <= self.lat <= 90.0):
            raise ValueError("緯度は-90.0から90.0の範囲で指定してください。")
        self.lon = float(self.lon)
        self.lat = float(self.lat)
