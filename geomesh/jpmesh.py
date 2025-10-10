"""
日本のメッシュコードに関するクラスと関数の定義
"""

import decimal
import math
from decimal import ROUND_DOWN, Decimal

import geopandas as gpd
import shapely
import yaml

from .data import Bounds
from .formatter import type_checker_float
from .geometries import dms_to_degree_lonlat

decimal.getcontext().prec = 13
decimal.getcontext().rounding = ROUND_DOWN


class MeshCodeJP(object):
    @type_checker_float(arg_index=1, kward="lon")
    @type_checker_float(arg_index=2, kward="lat")
    def __init__(self, lon: float, lat: float, is_dms: bool = False):
        if is_dms:
            # 経緯度がDMS形式の場合、度分秒を度に変換
            xy = dms_to_degree_lonlat(lon, lat)
            lon = xy.x  # type: ignore
            lat = xy.y  # type: ignore

        mesh = self._mesh_code(lon, lat)
        self.first_mesh_code: str = mesh["first_mesh_code"]
        self.secandary_mesh_code: str = mesh["secandary_mesh_code"]
        self.standard_mesh_code: str = mesh["standard_mesh_code"]
        self.half_mesh_code: str = mesh["half_mesh_code"]
        self.quarter_mesh_code: str = mesh["quarter_mesh_code"]

    def _mesh_code(self, lon: float, lat: float) -> dict[str, str]:
        """
        ## Description:
            この計算に使用されている1文字の変数名は[地域メッシュ統計の特質・沿革 p12]
            (https://www.stat.go.jp/data/mesh/pdf/gaiyo1.pdf)を参考にしています。
        ## Args:
            lon (float):
                経度（10進法）
            lat (float):
                緯度（10進法）
        ## Returns:
            dict[str, str]:
                メッシュコードの各部分を含む辞書
                - first_mesh_code: 第1次メッシュコード
                - secandary_mesh_code: 第2次メッシュコード
                - standard_mesh_code: 基準地域メッシュコード
                - half_mesh_code: 2分の1地域メッシュコード
                - quarter_mesh_code: 4分の1地域メッシュコード
        """
        # latitude
        p, a = divmod(lat * 60, 40)
        q, b = divmod(a, 5)
        r, c = divmod(b * 60, 30)
        s, d = divmod(c, 15)
        t, e = divmod(b, 7.5)
        first_lat_code = str(int(p))
        secandary_lat_code = str(int(q))
        standard_lat_code = str(int(r))
        # longitude
        f, i = math.modf(lon)
        u = int(i - 100)
        v, g = divmod(f * 60, 7.5)
        w, h = divmod(g * 60, 45)
        x, j = divmod(h, 22.5)
        y, j = divmod(j, 11.25)
        first_lon_code = str(int(u))
        secandary_lon_code = str(int(v))
        standard_lon_code = str(int(w))
        m = str(int((s * 2) + (x + 1)))
        n = str(int((t * 2) + (y + 1)))
        first_mesh_code = first_lat_code + first_lon_code
        secandary_mesh_code = first_mesh_code + secandary_lat_code + secandary_lon_code
        standard_mesh_code = secandary_mesh_code + standard_lat_code + standard_lon_code
        half_mesh_code = standard_mesh_code + m
        quarter_mesh_code = half_mesh_code + n
        return {
            "first_mesh_code": first_mesh_code,
            "secandary_mesh_code": secandary_mesh_code,
            "standard_mesh_code": standard_mesh_code,
            "half_mesh_code": half_mesh_code,
            "quarter_mesh_code": quarter_mesh_code,
        }

    def first_mesh(self) -> Bounds:
        """
        ## Summary:
            第1次メッシュの境界を取得する関数
        Returns:
            Bounds:
                第1次メッシュの境界
        """
        lat = int(self.first_mesh_code[0:2])
        lon = int(self.first_mesh_code[2:4]) + 100
        # 経度（x座標）: 第1次メッシュの経度方向の間隔は1度
        x_min = Decimal(f"{lon}")
        x_max = Decimal(f"{lon}") + 1
        # 緯度（y座標）: 第1次メッシュの緯度方向の間隔は40分（2/3度）
        y_min = Decimal(f"{lat}") * 40 / 60
        y_max = (Decimal(f"{lat}") + 1) * 40 / 60
        # Decimalをfloatに変換してBoundsに渡す
        return Bounds(float(x_min), float(y_min), float(x_max), float(y_max))

    def secandary_mesh(self) -> Bounds:
        """
        ## Summary:
            第2次メッシュの境界を取得する関数
        Returns:
            Bounds:
                第2次メッシュの境界
        """
        lat = Decimal(f"{int(self.secandary_mesh_code[0:2])}")
        lon = Decimal(f"{int(self.secandary_mesh_code[2:4])}") + 100
        lat_sec = Decimal(f"{int(self.secandary_mesh_code[4:5])}")
        lon_sec = Decimal(f"{int(self.secandary_mesh_code[5:6])}")
        # 経度（x座標）: 第2次メッシュの経度方向の間隔は7.5分（1/8度）
        x_min = lon + (lon_sec * Decimal("7.5") / 60)
        x_max = lon + ((lon_sec + 1) * Decimal("7.5") / 60)
        # 緯度（y座標）: 第2次メッシュの緯度方向の間隔は5分（1/12度）
        y_min = (lat * 40 / 60) + (lat_sec * Decimal("5") / 60)
        y_max = (lat * 40 / 60) + ((lat_sec + 1) * Decimal("5") / 60)
        return Bounds(float(x_min), float(y_min), float(x_max), float(y_max))

    def standard_mesh(self) -> Bounds:
        """
        ## Summary:
            基準地域メッシュの境界を取得する関数
        Returns:
            Bounds:
                基準地域メッシュの境界
        """
        lat = Decimal(f"{int(self.standard_mesh_code[0:2])}")
        lon = Decimal(f"{int(self.standard_mesh_code[2:4])}") + 100
        lat_sec = Decimal(f"{int(self.standard_mesh_code[4:5])}")
        lon_sec = Decimal(f"{int(self.standard_mesh_code[5:6])}")
        lat_std = Decimal(f"{int(self.standard_mesh_code[6:7])}")
        lon_std = Decimal(f"{int(self.standard_mesh_code[7:8])}")

        # 第2次メッシュ内の位置を計算
        sec_x_min = lon + (lon_sec * Decimal("7.5") / 60)
        sec_y_min = (lat * 40 / 60) + (lat_sec * Decimal("5") / 60)

        # 経度（x座標）: 基準地域メッシュの経度方向の間隔は45秒（0.75分）
        x_min = sec_x_min + (lon_std * Decimal("0.75") / 60)
        x_max = sec_x_min + ((lon_std + 1) * Decimal("0.75") / 60)

        # 緯度（y座標）: 基準地域メッシュの緯度方向の間隔は30秒（0.5分）
        y_min = sec_y_min + (lat_std * Decimal("0.5") / 60)
        y_max = sec_y_min + ((lat_std + 1) * Decimal("0.5") / 60)

        return Bounds(float(x_min), float(y_min), float(x_max), float(y_max))

    def half_mesh(self) -> Bounds:
        """
        ## Summary:
            2分の1地域メッシュの境界を取得する関数
        Returns:
            Bounds:
                2分の1地域メッシュの境界
        """
        half_code = int(self.half_mesh_code[8:9])

        # 基準地域メッシュの境界を計算
        standard_bounds = self.standard_mesh()
        std_x_min = Decimal(f"{standard_bounds.x_min}")
        std_y_min = Decimal(f"{standard_bounds.y_min}")

        # 2分の1メッシュのコード解析（1-4の値）
        # 1: 南西, 2: 南東, 3: 北西, 4: 北東
        if half_code == 1:  # 南西
            x_offset, y_offset = 0, 0
        elif half_code == 2:  # 南東
            x_offset, y_offset = 1, 0
        elif half_code == 3:  # 北西
            x_offset, y_offset = 0, 1
        elif half_code == 4:  # 北東
            x_offset, y_offset = 1, 1
        else:
            raise ValueError(f"Invalid half mesh code: {half_code}")

        # 経度（x座標）: 2分の1メッシュの経度方向の間隔は22.5秒（0.375分）
        x_min = std_x_min + (x_offset * Decimal("0.375") / 60)
        x_max = std_x_min + ((x_offset + 1) * Decimal("0.375") / 60)

        # 緯度（y座標）: 2分の1メッシュの緯度方向の間隔は15秒（0.25分）
        y_min = std_y_min + (y_offset * Decimal("0.25") / 60)
        y_max = std_y_min + ((y_offset + 1) * Decimal("0.25") / 60)

        return Bounds(float(x_min), float(y_min), float(x_max), float(y_max))

    def quarter_mesh(self) -> Bounds:
        """
        ## Summary:
            4分の1地域メッシュの境界を取得する関数
        Returns:
            Bounds:
                4分の1地域メッシュの境界
        """
        half_code = int(self.quarter_mesh_code[8:9])
        quarter_code = int(self.quarter_mesh_code[9:10])

        # 基準地域メッシュの境界を計算
        standard_bounds = self.standard_mesh()
        std_x_min = Decimal(f"{standard_bounds.x_min}")
        std_y_min = Decimal(f"{standard_bounds.y_min}")

        # 2分の1メッシュの境界を計算
        # 1: 南西, 2: 南東, 3: 北西, 4: 北東
        if half_code == 1:  # 南西
            half_x_offset, half_y_offset = 0, 0
        elif half_code == 2:  # 南東
            half_x_offset, half_y_offset = 1, 0
        elif half_code == 3:  # 北西
            half_x_offset, half_y_offset = 0, 1
        elif half_code == 4:  # 北東
            half_x_offset, half_y_offset = 1, 1
        else:
            raise ValueError(f"Invalid half mesh code: {half_code}")

        half_x_min = std_x_min + (half_x_offset * Decimal("0.375") / 60)
        half_y_min = std_y_min + (half_y_offset * Decimal("0.25") / 60)

        # 4分の1メッシュのコード解析（1-4の値）
        # 1: 南西, 2: 南東, 3: 北西, 4: 北東
        if quarter_code == 1:  # 南西
            quarter_x_offset, quarter_y_offset = 0, 0
        elif quarter_code == 2:  # 南東
            quarter_x_offset, quarter_y_offset = 1, 0
        elif quarter_code == 3:  # 北西
            quarter_x_offset, quarter_y_offset = 0, 1
        elif quarter_code == 4:  # 北東
            quarter_x_offset, quarter_y_offset = 1, 1
        else:
            raise ValueError(f"Invalid quarter mesh code: {quarter_code}")

        # 経度（x座標）: 4分の1メッシュの経度方向の間隔は11.25秒（0.1875分）
        x_min = half_x_min + (quarter_x_offset * Decimal("0.1875") / 60)
        x_max = half_x_min + ((quarter_x_offset + 1) * Decimal("0.1875") / 60)

        # 緯度（y座標）: 4分の1メッシュの緯度方向の間隔は7.5秒（0.125分）
        y_min = half_y_min + (quarter_y_offset * Decimal("0.125") / 60)
        y_max = half_y_min + ((quarter_y_offset + 1) * Decimal("0.125") / 60)

        return Bounds(float(x_min), float(y_min), float(x_max), float(y_max))

    def __str__(self) -> str:
        data = {
            "first_mesh_code": self.first_mesh_code,
            "secandary_mesh_code": self.secandary_mesh_code,
            "standard_mesh_code": self.standard_mesh_code,
            "half_mesh_code": self.half_mesh_code,
            "quarter_mesh_code": self.quarter_mesh_code,
        }
        return yaml.dump(data, allow_unicode=True, sort_keys=False)


def generate_jpmesh(
    x_min: float, y_min: float, x_max: float, y_max: float, mesh_size: str
) -> gpd.GeoDataFrame:
    """
    ## Summary:
        指定された範囲内で、指定の地域メッシュを生成する関数。
    Args:
        x_min (float):
            範囲の最小経度（10進法）
        y_min (float):
            範囲の最小緯度（10進法）
        x_max (float):
            範囲の最大経度（10進法）
        y_max (float):
            範囲の最大緯度（10進法）
        mesh_size (str):
            生成するメッシュのサイズ。'1st', '2nd', 'standard', 'half', 'quarter'のいずれか。
    Returns:
        gpd.GeoDataFrame:
            生成された地域メッシュのGeoDataFrame
    """
    from shapely.geometry import Polygon

    # メッシュサイズの検証
    valid_sizes = ["1st", "2nd", "standard", "half", "quarter"]
    if mesh_size not in valid_sizes:
        raise ValueError(f"mesh_size must be one of {valid_sizes}, got: {mesh_size}")

    # 範囲の検証
    if x_min >= x_max or y_min >= y_max:
        raise ValueError("Invalid range: min values must be less than max values")

    # メッシュ

    meshes = []
    mesh_codes = []

    # メッシュサイズに応じた処理分岐
    if mesh_size == "1st":
        # 第1次メッシュの生成
        lat_start = int(y_min * 60 / 40)
        lat_end = int(y_max * 60 / 40) + 1
        lon_start = int(x_min) - 100
        lon_end = int(x_max) - 100 + 1

        for lat_code in range(lat_start, lat_end):
            for lon_code in range(lon_start, lon_end):
                if lat_code < 0 or lon_code < 0:
                    continue

                mesh_code = f"{lat_code:02d}{lon_code:02d}"

                # メッシュ境界を計算
                mesh_obj = MeshCodeJP(
                    100 + lon_code + 0.5, lat_code * 40 / 60 + 20 / 60, False
                )
                if mesh_obj.first_mesh_code == mesh_code:
                    bounds = mesh_obj.first_mesh()

                    # 範囲内かチェック
                    polygon = Polygon(
                        [
                            (bounds.x_min, bounds.y_min),
                            (bounds.x_max, bounds.y_min),
                            (bounds.x_max, bounds.y_max),
                            (bounds.x_min, bounds.y_max),
                        ]
                    )
                    meshes.append(polygon)
                    mesh_codes.append(mesh_code)

    elif mesh_size == "2nd":
        # 第2次メッシュの生成
        _generate_mesh_grid(x_min, y_min, x_max, y_max, "2nd", meshes, mesh_codes)

    elif mesh_size == "standard":
        # 基準地域メッシュの生成
        _generate_mesh_grid(x_min, y_min, x_max, y_max, "standard", meshes, mesh_codes)

    elif mesh_size == "half":
        # 2分の1地域メッシュの生成
        _generate_mesh_grid(x_min, y_min, x_max, y_max, "half", meshes, mesh_codes)

    elif mesh_size == "quarter":
        # 4分の1地域メッシュの生成
        _generate_mesh_grid(x_min, y_min, x_max, y_max, "quarter", meshes, mesh_codes)

    # GeoDataFrameを作成
    gdf = gpd.GeoDataFrame(
        {"mesh_code": mesh_codes, "geometry": meshes}, crs="EPSG:4326"
    )

    return gdf


def _generate_mesh_grid(
    x_min: float,
    y_min: float,
    x_max: float,
    y_max: float,
    mesh_size: str,
    meshes: list,
    mesh_codes: list,
):
    """
    ## Summary:
        メッシュグリッドを生成するヘルパー関数
    """

    # サンプリング間隔を決定（メッシュサイズの1/4程度）
    if mesh_size == "2nd":
        step = 0.02  # 約2分間隔
    elif mesh_size == "standard":
        step = 0.002  # 約0.2分間隔
    elif mesh_size == "half":
        step = 0.001  # 約0.1分間隔
    elif mesh_size == "quarter":
        step = 0.0005  # 約0.05分間隔
    else:
        step = 0.01

    processed_codes = set()

    # サンプリング範囲を少し拡張して境界のメッシュを確実に取得
    # メッシュサイズに応じた適切な拡張量を設定
    if mesh_size == "2nd":
        margin = 0.1  # 第2次メッシュサイズの約1.5倍
    elif mesh_size == "standard":
        margin = 0.015  # 基準地域メッシュサイズの約1.5倍
    elif mesh_size == "half":
        margin = 0.008  # 2分の1メッシュサイズの約1.5倍
    elif mesh_size == "quarter":
        margin = 0.004  # 4分の1メッシュサイズの約1.5倍
    else:
        margin = 0.02

    # 拡張された範囲でサンプリング
    lat = y_min - margin
    while lat <= y_max + margin:
        lon = x_min - margin
        while lon <= x_max + margin:
            try:
                mesh_obj = MeshCodeJP(lon, lat, False)

                # メッシュサイズに応じてメッシュコードと境界を取得
                if mesh_size == "2nd":
                    code = mesh_obj.secandary_mesh_code
                    bounds = mesh_obj.secandary_mesh()
                elif mesh_size == "standard":
                    code = mesh_obj.standard_mesh_code
                    bounds = mesh_obj.standard_mesh()
                elif mesh_size == "half":
                    code = mesh_obj.half_mesh_code
                    bounds = mesh_obj.half_mesh()
                elif mesh_size == "quarter":
                    code = mesh_obj.quarter_mesh_code
                    bounds = mesh_obj.quarter_mesh()
                else:
                    lon += step
                    continue

                # 重複チェック
                if code not in processed_codes:
                    # 範囲内チェック
                    if (
                        bounds.x_max > x_min
                        and bounds.x_min < x_max
                        and bounds.y_max > y_min
                        and bounds.y_min < y_max
                    ):
                        polygon = shapely.box(*bounds)
                        meshes.append(polygon)
                        mesh_codes.append(code)
                        processed_codes.add(code)

            except (ValueError, ZeroDivisionError):
                # 無効な座標の場合はスキップ
                pass

            lon += step
        lat += step
