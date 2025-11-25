"""
Tests for Japanese mesh code functions (jpmesh module).
"""

import geopandas as gpd
import pytest

from geomesh.data import Bounds
from geomesh.jpmesh import MeshCodeJP, generate_jpmesh, mesh_code_to_bounds


class TestMeshCodeJP:
    """Tests for MeshCodeJP class."""

    def test_initialization_tokyo(self, tokyo_coords):
        """東京の座標でメッシュコードを生成"""
        mesh = MeshCodeJP(tokyo_coords.x, tokyo_coords.y)
        assert mesh.first_mesh_code is not None
        assert mesh.secandary_mesh_code is not None
        assert mesh.standard_mesh_code is not None
        assert mesh.half_mesh_code is not None
        assert mesh.quarter_mesh_code is not None

    def test_mesh_code_lengths(self, tokyo_coords):
        """各メッシュコードの長さが正しいか"""
        mesh = MeshCodeJP(tokyo_coords.x, tokyo_coords.y)
        assert len(mesh.first_mesh_code) == 4
        assert len(mesh.secandary_mesh_code) == 6
        assert len(mesh.standard_mesh_code) == 8
        assert len(mesh.half_mesh_code) == 9
        assert len(mesh.quarter_mesh_code) == 10

    def test_mesh_code_hierarchy(self, tokyo_coords):
        """メッシュコードの階層性（上位コードが下位コードに含まれる）"""
        mesh = MeshCodeJP(tokyo_coords.x, tokyo_coords.y)
        assert mesh.secandary_mesh_code.startswith(mesh.first_mesh_code)
        assert mesh.standard_mesh_code.startswith(mesh.secandary_mesh_code)
        assert mesh.half_mesh_code.startswith(mesh.standard_mesh_code)
        assert mesh.quarter_mesh_code.startswith(mesh.half_mesh_code)

    def test_first_mesh_bounds(self, tokyo_coords):
        """第1次メッシュの境界が正しく計算される"""
        mesh = MeshCodeJP(tokyo_coords.x, tokyo_coords.y)
        bounds = mesh.first_mesh()

        assert bounds.x_min < tokyo_coords.x <= bounds.x_max
        assert bounds.y_min < tokyo_coords.y <= bounds.y_max
        # 第1次メッシュのサイズチェック（約80km）
        assert abs(bounds.x_max - bounds.x_min - 1.0) < 0.01  # 経度1度
        assert abs(bounds.y_max - bounds.y_min - (2 / 3)) < 0.01  # 緯度40分

    def test_secandary_mesh_bounds(self, tokyo_coords):
        """第2次メッシュの境界が正しく計算される"""
        mesh = MeshCodeJP(tokyo_coords.x, tokyo_coords.y)
        bounds = mesh.secandary_mesh()

        assert bounds.x_min < tokyo_coords.x <= bounds.x_max
        assert bounds.y_min < tokyo_coords.y <= bounds.y_max
        # 第2次メッシュのサイズチェック
        assert abs(bounds.x_max - bounds.x_min - 0.125) < 0.001  # 7.5分

    def test_standard_mesh_bounds(self, tokyo_coords):
        """基準地域メッシュの境界が正しく計算される"""
        mesh = MeshCodeJP(tokyo_coords.x, tokyo_coords.y)
        bounds = mesh.standard_mesh()

        assert bounds.x_min < tokyo_coords.x <= bounds.x_max
        assert bounds.y_min < tokyo_coords.y <= bounds.y_max
        # 基準地域メッシュのサイズチェック
        assert abs(bounds.x_max - bounds.x_min - 0.0125) < 0.0001  # 45秒

    def test_half_mesh_bounds(self, tokyo_coords):
        """2分の1地域メッシュの境界が正しく計算される"""
        mesh = MeshCodeJP(tokyo_coords.x, tokyo_coords.y)
        bounds = mesh.half_mesh()

        assert bounds.x_min < tokyo_coords.x <= bounds.x_max
        assert bounds.y_min < tokyo_coords.y <= bounds.y_max

    def test_quarter_mesh_bounds(self, tokyo_coords):
        """4分の1地域メッシュの境界が正しく計算される"""
        mesh = MeshCodeJP(tokyo_coords.x, tokyo_coords.y)
        bounds = mesh.quarter_mesh()

        assert bounds.x_min < tokyo_coords.x <= bounds.x_max
        assert bounds.y_min < tokyo_coords.y <= bounds.y_max

    def test_mesh_nesting(self, tokyo_coords):
        """メッシュが入れ子構造になっているか"""
        mesh = MeshCodeJP(tokyo_coords.x, tokyo_coords.y)

        first = mesh.first_mesh()
        second = mesh.secandary_mesh()
        standard = mesh.standard_mesh()
        half = mesh.half_mesh()
        quarter = mesh.quarter_mesh()

        # 下位メッシュは上位メッシュに含まれる
        assert first.x_min <= second.x_min
        assert first.x_max >= second.x_max
        assert first.y_min <= second.y_min
        assert first.y_max >= second.y_max

        assert second.x_min <= standard.x_min
        assert second.x_max >= standard.x_max
        assert second.y_min <= standard.y_min
        assert second.y_max >= standard.y_max

        assert standard.x_min <= half.x_min
        assert standard.x_max >= half.x_max
        assert standard.y_min <= half.y_min
        assert standard.y_max >= half.y_max

        assert half.x_min <= quarter.x_min
        assert half.x_max >= quarter.x_max
        assert half.y_min <= quarter.y_min
        assert half.y_max >= quarter.y_max


class TestGenerateJPMesh:
    """Tests for generate_jpmesh function."""

    def test_generate_standard_mesh(self, small_bounds):
        """基準地域メッシュの生成"""
        gdf = generate_jpmesh(
            small_bounds.x_min,
            small_bounds.y_min,
            small_bounds.x_max,
            small_bounds.y_max,
            mesh_name="standard",
        )

        assert isinstance(gdf, gpd.GeoDataFrame)
        assert len(gdf) > 0
        assert "mesh_code" in gdf.columns
        assert "geometry" in gdf.columns
        # すべてのメッシュコードが8桁
        assert all(len(code) == 8 for code in gdf["mesh_code"])

    def test_generate_first_mesh(self, test_bounds):
        """第1次メッシュの生成"""
        gdf = generate_jpmesh(
            test_bounds.x_min,
            test_bounds.y_min,
            test_bounds.x_max,
            test_bounds.y_max,
            mesh_name="1st",
        )

        assert isinstance(gdf, gpd.GeoDataFrame)
        assert len(gdf) > 0
        assert all(len(code) == 4 for code in gdf["mesh_code"])

    def test_generate_second_mesh(self, small_bounds):
        """第2次メッシュの生成"""
        gdf = generate_jpmesh(
            small_bounds.x_min,
            small_bounds.y_min,
            small_bounds.x_max,
            small_bounds.y_max,
            mesh_name="2nd",
        )

        assert isinstance(gdf, gpd.GeoDataFrame)
        assert len(gdf) > 0
        assert all(len(code) == 6 for code in gdf["mesh_code"])

    def test_no_duplicate_mesh_codes(self, small_bounds):
        """重複したメッシュコードが生成されない"""
        gdf = generate_jpmesh(
            small_bounds.x_min,
            small_bounds.y_min,
            small_bounds.x_max,
            small_bounds.y_max,
            mesh_name="standard",
        )

        assert len(gdf["mesh_code"]) == len(gdf["mesh_code"].unique())

    def test_invalid_mesh_name(self, small_bounds):
        """無効なメッシュ名でエラーが発生"""
        with pytest.raises(ValueError):
            generate_jpmesh(
                small_bounds.x_min,
                small_bounds.y_min,
                small_bounds.x_max,
                small_bounds.y_max,
                mesh_name="invalid",
            )

    def test_invalid_range(self):
        """無効な範囲でエラーが発生"""
        with pytest.raises(ValueError):
            generate_jpmesh(
                140.0,  # x_min > x_max
                35.0,
                139.0,
                36.0,
                mesh_name="standard",
            )

    def test_crs_is_correct(self, small_bounds):
        """生成されたGeoDataFrameのCRSが正しい"""
        gdf = generate_jpmesh(
            small_bounds.x_min,
            small_bounds.y_min,
            small_bounds.x_max,
            small_bounds.y_max,
            mesh_name="standard",
        )

        assert gdf.crs == "EPSG:4326"


class TestMeshCodeToBounds:
    """Tests for mesh_code_to_bounds function."""

    def test_first_mesh_code_to_bounds(self, known_mesh_codes):
        """第1次メッシュコードから境界を取得"""
        tokyo_data = known_mesh_codes["tokyo_standard"]
        first_code = tokyo_data["codes"]["first"]

        bounds = mesh_code_to_bounds(first_code)
        assert isinstance(bounds, Bounds)
        assert bounds.x_min < bounds.x_max
        assert bounds.y_min < bounds.y_max

    def test_invalid_mesh_code(self):
        """無効なメッシュコードでエラーが発生"""
        with pytest.raises(ValueError):
            mesh_code_to_bounds("123")  # 長さが不正

    def test_roundtrip_conversion(self, tokyo_coords):
        """メッシュコード生成→境界取得→元の座標が含まれる"""
        mesh = MeshCodeJP(tokyo_coords.x, tokyo_coords.y)
        bounds = mesh_code_to_bounds(mesh.standard_mesh_code)

        assert bounds.x_min < tokyo_coords.x <= bounds.x_max
        assert bounds.y_min < tokyo_coords.y <= bounds.y_max
