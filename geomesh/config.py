"""
各種設定の定義
"""

from typing import NamedTuple


class JprBounds(NamedTuple):
    """
    ## Summary:
        日本の平面直角座標系に変換可能な範囲を表すクラス。この範囲は``pyproj``のCRSオブジェ
        クトの``area_of_use``属性に基づいています。
    """

    lat_max: float = 45.55
    lat_min: float = 20.36
    lon_max: float = 154.06
    lon_min: float = 122.82
