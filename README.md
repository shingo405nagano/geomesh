

### タイル座標の確認
```python
import geomesh

>>> lon = 139.767125
>>> lat = 35.681236
>>> zl = 15
>>> geomesh.tile_designer.lonlat_to_tile_idx(lon, lat, zl, "EPSG:4326")
{'x': 29105, 'y': 12903}

```

### 経緯度からタイルの情報を取得
```python
import geomesh
>>> lon = 139.767125
>>> lat = 35.681236
>>> zl = 15
>>> tile = geomesh.tile_designer.design_from_lonlat(lon, lat, zl, "EPSG:4326")
>>> print(tile)
type: <class 'geomesh.glmesh.TileDesign'>
crs:
  name: WGS 84 / Pseudo-Mercator
  epsg: 3857
  unit: metre
XYZ:
  x_idx: 29105
  y_idx: 12903
  zoom_level: 15
bounds:
  x_min: 15557686.989
  y_min: 4257236.7273
  x_max: 15558909.9815
  y_max: 4256013.7349
resolution:
  x_resolution [m/px]: 4.7773
  y_resolution [m/px]: -4.7774
```

### タイルインデックスからタイルの情報を取得
```python
import geomesh
>>> x_idx = 29105
>>> y_idx = 12903
>>> zl = 15
>>> tile = geomesh.tile_designer.design_from_tile_idx(x_idx, y_idx, zl, "EPSG:4326")
>>> print(tile)
type: <class 'geomesh.glmesh.TileDesign'>
crs:
  name: WGS 84 / Pseudo-Mercator
  epsg: 3857
  unit: metre
XYZ:
  x_idx: 29105
  y_idx: 12903
  zoom_level: 15
bounds:
  x_min: 15557686.989
  y_min: 4257236.7273
  x_max: 15558909.9815
  y_max: 4256013.7349
resolution:
  x_resolution [m/px]: 4.7773
  y_resolution [m/px]: -4.7774
```

### 指定した範囲のタイル情報を取得
```python
import geomesh
>>> x_min = 140.6118737
>>> x_max = 140.6136660
>>> y_min = 40.8367183
>>> y_max = 40.8381160
>>> zl = 18
>>> tiles = geomesh.tile_designer.design_tiles(x_min, y_min, x_max, y_max, zl, "EPSG:4326", geodataframe=True)
>>> print(tiles)
   zoom_level   x_idx  y_idx  x_resolution  y_resolution                                           geometry
0          18  233462  98440        0.5971       -0.5972  POLYGON ((15652927.526 4988586.214, 15652927.5...
1          18  233462  98441        0.5971       -0.5972  POLYGON ((15652927.526 4988433.34, 15652927.52...
2          18  233463  98440        0.5971       -0.5972  POLYGON ((15653080.4 4988586.214, 15653080.4 4...
3          18  233463  98441        0.5971       -0.5972  POLYGON ((15653080.4 4988433.34, 15653080.4 49...
```