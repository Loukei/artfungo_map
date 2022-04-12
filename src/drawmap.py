'''
input: 從儲存的CSV檔案讀取店家資訊
output: 輸出Foulium地圖

## TODO
- 讀取CSV檔
- 每讀到一個正確的位址,建立一個marker同時計算bBox
- 讀完後同時取得marker_list與bBox範圍

'''

import folium
from pathlib import Path
from datetime import datetime,timezone
import os
import webbrowser

def test_locations():
    "define test data"
    r = [
        {"name": "大人物書店", "lat": 23.4718747, "lng": 120.4607824},
        {"name": "三福書城", "lat": 23.4779863, "lng": 120.4573471},
        {"name": "天才書局", "lat": 23.4624972, "lng": 120.4532138},
        {"name": "金冠文化廣場", "lat": 23.476856, "lng": 120.4594929},
        ]
    return r

def create_output_map_path(input_file_path:str,output_folder:str) -> Path:
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
    return output_folder_P.joinpath(timestamp + input_file_P.stem).with_suffix('.html')

def compute_map_bBox(box:list,latlng:tuple) -> list:
    "計算地圖的範圍,回傳新的bounding box [(-90.0,-180.0),(90.0,180.0)]"
    lat:float = latlng[0]
    lng:float = latlng[1]
    latMin:float = lat if lat < box[0][0] else box[0][0]
    lngMin:float = lng if lng < box[0][1] else box[0][1]
    latMax:float = lat if lat > box[1][0] else box[1][0]
    lngMax:float = lng if lng > box[1][1] else box[1][1]
    return [(latMin,lngMin),(latMax,lngMax)]

def compute_map_center(box:list,ndigits: int)  -> tuple:
    "計算地圖中心點"
    lat = round( (box[1][0] - box[0][0]) / 2 , ndigits) # (lat_max - lat_min)/2 取至第ndigits位
    lng = round((box[1][1] - box[0][1]) / 2 , ndigits) # (lng_max - lng_min)/2
    return (lat,lng)

def add_map_markers():
    "把檔案的地標加入地圖內"
    pass

def open_file_on_browser(output_file_path:str) -> None:
    """Open map {output_file_path} from user default browser.

    Args:
        output_file_path (str): _description_
    """
    abs_path = os.path.abspath(output_file_path)
    print(f'Open map: <{abs_path}>')
    webbrowser.open(abs_path)
    pass

def main(input_file_path:str,output_folder:str):
    try:
        newfilename:str = create_output_map_path(input_file_path,output_folder).as_posix()
        print(f"new file name: <{newfilename}>")
        map_center = [23.476856,120.4594929] # 嘉義火車站
        fmap = folium.Map(location=map_center, zoom_start=16, tiles="OpenStreetMap")
        # --- fmap.location 可以事後修改 ---
        # --- 讀取地址資料並同時計算bBox與中心點
        # TODO
        stores = test_locations()
        bBox = [(90.0,180.0),(-90.0,-180.0)]
        for store in stores:
            if(store["lat"] and store["lng"]):
                bBox = compute_map_bBox(box=bBox,latlng=(store["lat"],store["lng"]))
            pass
        fmap.fit_bounds(bounds=bBox)
        fmap.location = compute_map_center(box=bBox, ndigits=5)
        print(fmap.location)
        # ---
        fmap.save(newfilename)
        open_file_on_browser(newfilename)
        os.system('PAUSE')
    except Exception as e:
        print(e)
    pass

if __name__ == "__main__":
    input_file_path: str = "testdata\嘉義市書店地圖.csv"
    output_folder: str = "testdata\output"
    main(input_file_path,output_folder)
    pass