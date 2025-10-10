from typing import Iterable

import pyproj

from .data import XY
from .formatter import type_checker_crs, type_checker_float


@type_checker_float(arg_index=0, kward="x")
@type_checker_float(arg_index=1, kward="y")
@type_checker_crs(arg_index=2, kward="in_crs")
@type_checker_crs(arg_index=3, kward="out_crs")
def transform_xy(
    x: float | Iterable[float],  #
    y: float | Iterable[float],
    in_crs: str | int | pyproj.CRS,
    out_crs: str | int | pyproj.CRS,
) -> XY | list[XY]:
    """
    ## Summary:
        x座標とy座標を指定した座標系から別の座標系に変換する。
    Args:
        x (float | Iterable[float]):
            変換するx座標。単一の値または値のリスト。
        y (float | Iterable[float]):
            変換するy座標。単一の値または値のリスト。
        in_crs (str | int | pyproj.CRS):
            入力座標系。EPSGコードやCRSオブジェクトを指定。
        out_crs (str | int | pyproj.CRS):
            出力座標系。EPSGコードやCRSオブジェクトを指定。
    Returns:
        XY | list[XY]:
            変換後の座標。単一のXYオブジェクトまたはXYオブジェクトのリスト。
    """
    transformer = pyproj.Transformer.from_crs(in_crs, out_crs, always_xy=True)
    lon, lat = transformer.transform(x, y)
    if isinstance(x, Iterable):
        return [XY(x=lon_i, y=lat_i) for lon_i, lat_i in zip(lon, lat, strict=False)]
    return XY(x=lon, y=lat)
