# Geo-Mesh
**Geo-Mesh**は、GIS（地理情報システム）で使用する、メッシュグリッドを生成・操作するためのPythonライブラリです。メッシュグリッドは特定の地域を隙間なく定量的に分割し、地理空間データの解析や可視化に役立ちます。

 - **第1次地域区画** ... 日本全国の地域を偶数緯度及びその間隔（120分）を3等分した緯度における緯線並びに1度ごとの経線とによって分割してできる区域

 - **第2次地域区画** ... 第1次地域区画を緯線方向及び経線方向に8等分してできる区域

 - **基準地域メッシュ** ... 第2次地域区画を緯線方向及び経線方向に10等分してできる区域

 - **2分の1地域メッシュ** ... 基準地域メッシュ（第3次地域区画）を緯線方向、経線方向に2等分してできる区域

 - **4分の1地域メッシュ** ... 2分の1地域メッシュを緯線方向、経線方向に2等分してできる区域

 - **Globalメッシュ** ... GISで使用される"タイル"の分割線として使用されるメッシュグリッド。ここでいうタイルは``slippy map tilenames``形式のタイルを指します。このメッシュはZoomLevel（ズームレベル）に基づいて分割され、ほぼ世界中をカバーします。


## 2. 地域メッシュ（日本国内）

### 2-1. 地域メッシュとは
地域メッシュ統計とは、緯度・経度に基づき地域を隙間なく網の目（メッシュ）の区域に分けて、それぞれの区域に関する統計データを編成したものです。

作成された地域メッシュ統計には次のような利点があります。

 - 地域メッシュは、ほぼ同一の大きさ及び形状の区画を単位として区分されているので、地域メッシュ相互間の事象の計量的比較が容易です。
 - 地域メッシュは、その位置や区画が固定されていることから、市町村などの行政区域の境域変更や地形、地物の変化による調査区の設定変更などの影響を受けることがなく、地域事象の時系列的比較が容易です。
 - 地域メッシュのデータを合算することにより、任意の地域について必要なデータの入手が容易です。
 - 地域メッシュは、緯度・経度に基づき区画されたほぼ正方形の形状であることから、位置の表示が明確で簡便にできるので、距離に関連した分析・計算・比較が容易です。

<table border="1" cellpadding="3" cellspacing="0" class="datatable" width="650"> 
       <caption> <strong>地域メッシュの区分方法</strong> 
       </caption> 
       <tbody> 
        <tr align="center"> 
         <th style="width: 200px;">区画の種類</th> 
         <th style="width: 250px;">区分方法</th> 
         <th style="width: 50px;">緯度の間隔</th> 
         <th style="width: 50px;">経度の<br> 間隔</th> 
         <th>一辺の長さ</th> 
         <th style="width: 150px;">地図との関係</th> 
        </tr> 
        <tr> 
         <td>第1次地域区画</td> 
         <td>全国の地域を偶数緯度及びその間隔（120分）を3等分した緯度における緯線並びに1度ごとの経線とによって分割してできる区域</td> 
         <td align="right">40分</td> 
         <td align="right">1度</td> 
         <td align="right">約80km</td> 
         <td>20万分の1地勢図の1図葉の区画</td> 
        </tr> 
        <tr> 
         <td>第2次地域区画<br> （統合地域メッシュ）</td> 
         <td>第1次地域区画を緯線方向及び経線方向に8等分してできる区域</td> 
         <td align="right">5分</td> 
         <td align="right">7分<br> 30秒</td> 
         <td align="right">約10km</td> 
         <td>2万5千分の1地勢図の1図葉の区画</td> 
        </tr> 
        <tr> 
         <td>基準地域メッシュ<br> （第3次地域区画）</td> 
         <td>第2次地域区画を緯線方向及び経線方向に10等分してできる区域</td> 
         <td align="right">30秒</td> 
         <td align="right">45秒</td> 
         <td align="right">約1km</td> 
         <td>&nbsp;</td> 
        </tr> 
        <tr> 
         <td>2分の1地域メッシュ<br> （分割地域メッシュ）</td> 
         <td>基準地域メッシュ（第3次地域区画）を緯線方向、経線方向に2等分してできる区域</td> 
         <td align="right">15秒</td> 
         <td align="right">22.5秒</td> 
         <td align="right">約500m</td> 
         <td>&nbsp;</td> 
        </tr> 
        <tr> 
         <td>4分の1地域メッシュ<br> （分割地域メッシュ）</td> 
         <td>2分の1地域メッシュを緯線方向、経線方向に2等分してできる区域</td> 
         <td align="right">7.5秒</td> 
         <td align="right">11.25秒</td> 
         <td align="right">約250m</td> 
         <td>&nbsp;</td> 
        </tr> 
       </tbody> 
      </table>

※ 出典：総務省統計局「地域メッシュ統計について」 https://www.stat.go.jp/data/mesh/m_tuite.html

※ 総務省統計局「地域メッシュ統計の特質・沿革」 https://www.stat.go.jp/data/mesh/pdf/gaiyo1.pdf

※ 総務省統計局「地域メッシュ統計の作成」 https://www.stat.go.jp/data/mesh/pdf/gaiyo2.pdf


### 2-2. 10進経緯度から地域メッシュコードを取得
```python
>>> import geomesh
>>> lon = 140.467194155
>>> lat = 40.596179690
>>> mesh_jp = geomesh.MeshCodeJP(lon, lat)
>>> print(mesh_jp)

first_mesh_code: '6040'
secandary_mesh_code: '604073'
standard_mesh_code: '60407317'
half_mesh_code: '604073173'
quarter_mesh_code: '6040731732'
```

## 2-3. メッシュコードから区画の座標を取得

メッシュコードは文字列として渡し、桁数に応じた区画の範囲が返されます。
```python
>>> mesh_code = ["6040", "604073", "60407317", "604073173", "6040731732"]
>>> names = [
....    "第1次地域区画",
....    "第2次地域区画",
....    "基準地域メッシュ",
....    "2分の1地域メッシュ",
....    "4分の1地域メッシュ",
....  ]
>>> for code, name in zip(mesh_code, names):
....    mesh = geomesh.mesh_code_to_bounds(code)
....    print(name, "\n", mesh, "\n")

第1次地域区画 
 Bounds(x_min=140.0, y_min=39.999999996, x_max=141.0, y_max=40.6666666626) 

第2次地域区画 
 Bounds(x_min=140.375, y_min=40.5833333331, x_max=140.5, y_max=40.6666666664) 

基準地域メッシュ 
 Bounds(x_min=140.4625, y_min=40.5916666666, x_max=140.475, y_max=40.5999999999) 

2分の1地域メッシュ 
 Bounds(x_min=140.4625, y_min=40.5958333332, x_max=140.46875, y_max=40.5999999998) 

4分の1地域メッシュ 
 Bounds(x_min=140.465625, y_min=40.5958333332, x_max=140.46875, y_max=40.5979166665) 
```

### 2-4. 範囲内の地域メッシュコードをGeoDataFrameで取得
```python
>>> import geomesh
>>> lon_min, lat_min, lon_max, lat_max = (
....    140.467194155,
....    40.596179690,
....    141.002244644,
....    40.990309691,
....)
>>> mesh_gdf = geomesh.generate_jpmesh(
....    lon_min, lat_min, lon_max, lat_max, mesh_name="standard"
....)
>>> print(mesh_gdf)
     mesh_code                                           geometry
0     60407317  POLYGON ((140.475 40.59167, 140.475 40.6, 140....
1     60407327  POLYGON ((140.475 40.6, 140.475 40.60833, 140....
2     60407337  POLYGON ((140.475 40.60833, 140.475 40.61667, ...
3     60407347  POLYGON ((140.475 40.61667, 140.475 40.625, 14...
4     60407357  POLYGON ((140.475 40.625, 140.475 40.63333, 14...
...        ...                                                ...
2107  61413040  POLYGON ((141.0125 40.95, 141.0125 40.95833, 1...
2108  61413050  POLYGON ((141.0125 40.95833, 141.0125 40.96667...
2109  61413060  POLYGON ((141.0125 40.96667, 141.0125 40.975, ...
2110  61413070  POLYGON ((141.0125 40.975, 141.0125 40.98333, ...
2111  61413080  POLYGON ((141.0125 40.98333, 141.0125 40.99167...
```





















































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