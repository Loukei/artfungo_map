'''
input: 從儲存的CSV檔案讀取店家資訊
output: 輸出Foulium地圖

## TODO
- 使用一個類別(Store)來處理資料
    - 該類別可以讀取CSV檔中的資料
    - 驗證經緯度轉換是否成功
    - 輸出符合folium Marker格式的資料
'''

import folium
from pathlib import Path
from datetime import datetime,timezone
from os.path import abspath as os_path_abspath
from webbrowser import open as webbrowser_open
from typing import List,Dict

def test_markers() -> List[folium.Marker]:
    r = [
        folium.Marker(location = [23.4718747,120.4607824],popup = "嘉義市東區體育路29號",tooltip = "大人物書店"),
        folium.Marker(location = [23.4779863,120.4573471],popup = "嘉義市東區和平路227號",tooltip = "三福書城"),
        folium.Marker(location = [23.4624972,120.4532138],popup = "嘉義市東區大業街97號",tooltip = "天才書局"),
        folium.Marker(location = [23.476856,120.4594929],popup = "嘉義市東區民族路90號",tooltip = "金冠文化廣場"),
    ]
    return r

def create_output_map_path(input_file_path:str,output_folder:str) -> str:
    """將輸出路徑與輸入檔案結合產生預計要輸出的檔案名稱

    Args:
        input_file_path (str): _description_
        output_folder (str): _description_

    Raises:
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_

    Returns:
        Path: _description_
    """
    input_file_P = Path(input_file_path)
    output_folder_P = Path(output_folder)
    if(not input_file_P.is_file()):
        raise ValueError(f"Input file <{input_file_path}> is not a file.")
    if(not input_file_P.suffix == ".csv"):
        raise ValueError(f'Input file <{input_file_path}> is not a csv file')
    if(not output_folder_P.is_dir()):
        raise ValueError(f'Output folder <{output_folder}> is not a folder.')
    timestamp:str = datetime.strftime(datetime.now(tz=timezone.utc),"[%Y%m%d%z_%H'%M'%S]") # ex: "[20220412+0000_03'55'31]"
    return output_folder_P.joinpath(timestamp + input_file_P.stem).with_suffix('.html').as_posix()

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
    """ 檢查經度(lng)與緯度(lat)數字

    Args:
        lat (float): 緯度 -90.0 ~ 90.0
        lng (float): 經度 -180.0 ~ 180.0

    Returns:
        bool: _description_
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
    # --- 初始化地圖資料 ---
    map_center = [23.476856,120.4594929] # 嘉義火車站(暫時的地圖中心點)
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

# def draw_foluim_map(map_path:str,results:List[Dict]):
#     markers:List[folium.Marker] = [folium.Marker(location=r["location"],tooltip=r["describe"],popup=r["name"]) for r in results]
#     draw_foluim_map(map_path = map_path,markers = markers)
#     pass

def example(input_file_path:str,output_folder:str):
    try:
        map_path:str = create_output_map_path(input_file_path,output_folder)
        print(f"new map file name: <{map_path}>")
        markers:List[folium.Marker] = test_markers() # 產生範例
        draw_foluim_map(map_path,markers) # 利用 stores 建立地圖
    except Exception as e:
        print(e)
    pass

if __name__ == "__main__":
    filepath:str = "testdata\嘉義市書店地圖.csv"
    output_folder:str = "testdata\output"
    example(filepath,output_folder)
    pass