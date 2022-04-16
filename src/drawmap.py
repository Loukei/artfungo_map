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
from typing import TypedDict,List

class Store(TypedDict):
    """Define the Store info for foluim map marker

    Args:
        name:           Store name
        address:        House address
        lat:            latitude -90.0 ~ 90.0
        lng:            longitude -180.0 ~ 180.0
        phone_number:   phone number for store
    """
    name:str        
    address:str     
    lat:float
    lng:float
    phone_number:str

def test_locations():
    "define test data"
    r = [
        Store(name="大人物書店",address="嘉義市東區體育路29號",lat=23.4718747,lng=120.4607824,phone_number="05-2282648"),
        Store(name="三福書城",address="嘉義市東區和平路227號",lat=23.4779863,lng=120.4573471,phone_number="05-2280377"),
        Store(name="天才書局",address="嘉義市東區大業街97號",lat=23.4624972,lng=120.4532138,phone_number="05-2289560"),
        Store(name="金冠文化廣場",address="嘉義市東區民族路90號",lat=23.476856,lng=120.4594929,phone_number="05-2711669")
        ]
    return r

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

def craete_map_marker(store:Store) -> folium.Marker:
    """Create a folium.Marker by type Store
    
    產生Folium的地標(marker)
    
    Args:
        store (Store): 

    Returns:
        folium.Marker: 
    """
    location:list = [store["lat"],store["lng"]]
    tooltip:str = f'<h1><strong>{store["name"]}</strong></h1> <p>{store["address"]}</p> <p>{store["phone_number"]}</p>'
    popup:str = store["name"]
    return folium.Marker(location,tooltip,popup)

def open_file_on_browser(output_file_path:str) -> None:
    """Open map file {output_file_path} from user default browser.

    Args:
        output_file_path (str): _description_
    """
    abs_path = os_path_abspath(output_file_path)
    print(f'Open map: <{abs_path}>')
    webbrowser_open(abs_path)
    pass

def create_map(store_list: List[Store]) -> folium.Map:
    """Create map with placemark(List[Store])

    Args:
        store_list (List[Store]): _description_

    Returns:
        folium.Map: a datatype for folium to draw a map
    """
    # --- 初始化地圖資料 ---
    map_center = [23.476856,120.4594929] # 嘉義火車站(暫時的地圖中心點)
    bBox = [(90.0,180.0),(-90.0,-180.0)] # 整個地圖的地標範圍
    fmap:folium.Map = folium.Map(location=map_center, zoom_start=16, tiles="OpenStreetMap")
    # --- 讀取地圖資料 ---
    store:Store
    for store in store_list:
        geocode = [store["lat"],store["lng"]]
        if(check_geocode(store["lat"],store["lng"])):
            bBox = compute_map_bBox(box=bBox,latlng=geocode)
            marker:folium.Marker = craete_map_marker(store)
            marker.add_to(fmap)
        else:
            print(f'[ERROR]Store {store} is not a legal geocode.')
    # --- 將地圖重新套用bBox與地圖中心點 ---
    fmap.fit_bounds(bounds=bBox)
    fmap.location = compute_map_center(box=bBox, ndigits=5)
    return fmap

def create_map_v2(markers: List[folium.Marker]) -> folium.Map:
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

def write_foluim_map(map_path:str,stores:List[Store]):
    """Draw placemark(with type store) in foluim.Map

    Args:
        map_path (str): _description_
        stores (List[Store]): _description_
    """
    fmap:folium.Map = create_map(stores)
    fmap.save(map_path)
    open_file_on_browser(map_path)
    pass

def write_foluim_map_v2(map_path:str,markers:List[folium.Marker]):
    fmap:folium.Map = create_map_v2(markers)
    fmap.save(map_path)
    open_file_on_browser(map_path)
    pass

def example(input_file_path:str,output_folder:str):
    try:
        map_path:str = create_output_map_path(input_file_path,output_folder)
        print(f"new map file name: <{map_path}>")
        stores:List[Store] = test_locations() # 產生範例
        write_foluim_map(map_path,stores) # 利用 stores 建立地圖
    except Exception as e:
        print(e)
    pass

if __name__ == "__main__":
    filepath:str = "testdata\嘉義市書店地圖.csv"
    output_folder:str = "testdata\output"
    # example(filepath,output_folder)
    map_path = "testmap.html"
    markers:List[folium.Marker] = test_markers()
    fmap:folium.Map = create_map_v2(markers)
    fmap.save(map_path)
    open_file_on_browser(map_path)
    pass