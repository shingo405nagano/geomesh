"""
Dataクラスの定義
"""

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
