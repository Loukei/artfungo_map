'''
## Describe

給定List[folium.Marker],計算地圖中心點等等,輸出Foulium地圖,並且打開瀏覽器確認
- folium.Marker為foluim的地理標記類別

## Example

``` Python
markers:List[folium.Marker] = test_markers() # default test data markers
draw_foluim_map('map.html',markers)
```

## Reference

- [foluim - Markers](https://python-visualization.github.io/folium/quickstart.html#Markers)

'''

import folium
from os.path import abspath as os_path_abspath
from webbrowser import open as webbrowser_open
from typing import List

def test_markers() -> List[folium.Marker]:
    r = [
        folium.Marker(location = [23.4718747,120.4607824],popup = "嘉義市東區體育路29號",tooltip = "大人物書店"),
        folium.Marker(location = [23.4779863,120.4573471],popup = "嘉義市東區和平路227號",tooltip = "三福書城"),
        folium.Marker(location = [23.4624972,120.4532138],popup = "嘉義市東區大業街97號",tooltip = "天才書局"),
        folium.Marker(location = [23.476856,120.4594929],popup = "嘉義市東區民族路90號",tooltip = "金冠文化廣場"),
    ]
    return r

def compute_map_bBox(box:list,latlng:List) -> list:
    "計算地圖的範圍,回傳新的bounding box [(-90.0,-180.0),(90.0,180.0)]"
    lat:float = latlng[0]
    lng:float = latlng[1]
    latMin:float = lat if lat < box[0][0] else box[0][0]
    lngMin:float = lng if lng < box[0][1] else box[0][1]
    latMax:float = lat if lat > box[1][0] else box[1][0]
    lngMax:float = lng if lng > box[1][1] else box[1][1]
    return [(latMin,lngMin),(latMax,lngMax)]

def compute_map_center(box:list,ndigits: int)  -> tuple:
    """Compute the map center by {box}

    計算地圖中心點

    Args:
        box (list): [(latMin,lngMin),(latMax,lngMax)]
        ndigits (int): 取平均到(ndigits)位數

    Returns:
        tuple: a geocode with (lat,lng)
    """
    lat = round( (box[1][0] - box[0][0]) / 2 , ndigits) # (lat_max - lat_min)/2 取至第ndigits位
    lng = round((box[1][1] - box[0][1]) / 2 , ndigits) # (lng_max - lng_min)/2
    return (lat,lng)

def check_geocode(lat:float, lng: float) -> bool:
    """ 檢查經度(lng)與緯度(lat)的數字

    Args:
        lat (float): 緯度 -90.0 ~ 90.0
        lng (float): 經度 -180.0 ~ 180.0

    Returns:
        bool: 檢查正確回傳True,失敗回傳False
    """
    if(type(lat) is float and type(lng) is float):
        return (lat <= 90.0 and lat >= -90.0) and (lng <= 180.0 and lng >= -180.0)
    else:
        return False

def open_file_on_browser(output_file_path:str) -> None:
    """Open map file {output_file_path} from user default browser.

    Args:
        output_file_path (str): _description_
    """
    abs_path = os_path_abspath(output_file_path)
    print(f'Open map: <{abs_path}>')
    webbrowser_open(abs_path)
    pass

def create_map(markers: List[folium.Marker]) -> folium.Map:
    """Read the List of Marker {markers}, fill the data to map

    Args:
        markers (List[folium.Marker]): the List of Marker

    Returns:
        folium.Map: The map ready to save or edit.
    """
    # --- 初始化地圖資料 ---
    map_center = [23.476856,120.4594929] # 地圖中心點(嘉義火車站)
    bBox = [(90.0,180.0),(-90.0,-180.0)] # 整個地圖的地標範圍
    fmap:folium.Map = folium.Map(location=map_center, zoom_start=16, tiles="OpenStreetMap")
    # --- 讀取地圖資料 ---
    marker:folium.Marker
    for marker in markers:
        location = marker.location
        if(check_geocode(location[0],location[1])):
            bBox = compute_map_bBox(box=bBox,latlng=location)
            marker.add_to(fmap)
        else:
            print(f'[ERROR]Store {marker} is not a legal geocode.')
    # --- 將地圖重新套用bBox與地圖中心點 ---
    fmap.fit_bounds(bounds=bBox)
    fmap.location = compute_map_center(box=bBox, ndigits=5)
    return fmap

def draw_foluim_map(map_path:str,markers:List[folium.Marker]):
    """Draw a map from a dict

    Args:
        map_path (str): _description_
        markers (List[folium.Marker]): _description_
    """
    fmap:folium.Map = create_map(markers)
    fmap.save(map_path)
    open_file_on_browser(map_path)
    pass

if __name__ == "__main__":
    markers:List[folium.Marker] = test_markers() # 產生範例
    draw_foluim_map("testmap.html",markers) # 利用 markers 建立地圖
    pass