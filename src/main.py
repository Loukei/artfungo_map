'''
## Describe

## Process

1. 讀取店家CSV資料
2. 將店家地址轉成經緯度儲存
3. 使用經緯度資訊與店家資訊,產生HTML地圖
4. 開啟地圖
5. (可選)輸出KML格式資料

## Usage

- 建立一個 `.env`檔案,包含以下值"BINGMAP_API_KEY = YOUR_API_KEY"
- 針對你的CSV檔格式
    - csv檔案第一列必須註明資料欄位名稱
    - 修改`fieldnames = ["行政區","店名","地址","電話","坐標(緯度)","坐標(經度)"]`以符合你的欄位名稱
    - 修改`address_name`,指向你的地址欄位名稱如"地址"
    - 撰寫一個函數將輸出的報告`results`轉換成`writekml.PlaceMark`,參考`convert_geocoding_result_to_palcemark()`

## Note

以我使用Bing Map的經驗, batch geocoding是較不推薦的方式
- 回應時間較長
- 只會回傳經緯度數值,不會有錯誤訊息與比對結果
- 處理大型檔案時這種方式不適用
'''

#!/usr/bin/python3
import csv
from pathlib import Path
from typing import List,Dict
from os import getenv as os_getenv
from dotenv import load_dotenv # read api key from (.env) file 
from datetime import datetime,timezone
import geocoding
import writekml
import folium 
import drawmap

def convert_geocoding_result_to_palcemark(result:Dict) -> writekml.PlaceMark:
    """將地址轉經緯度的報告轉成PlaceMark

    Detail:
        PlaceMark主要用來儲存三個訊息: 經緯度(lat,lng),地標名稱(name),詳細描述(describe)
        不管在輸出kml或folium地圖所需的參數就只需這三個,但是使用者必須根據來源的csv格式親自處理這些轉換

    Args:
        result (Dict): _description_

    Returns:
        writekml.PlaceMark: 包含地點資訊的字典 ex: {"name":"","describe":"","lat":0.0,"lng":0.0}
    """
    describe:str = f'Name: {result["店名"]}, Address: {result["地址"]}, Phone_number: {result["電話"]}'
    return writekml.PlaceMark(name=result["店名"],describe=describe,lat=result["坐標(緯度)"],lng=result["坐標(經度)"])

def placemark_to_foluimMarker(placemark:writekml.PlaceMark) -> folium.Marker:
    return folium.Marker(location=[placemark["lat"],placemark["lng"]],popup=placemark["describe"],tooltip=placemark["name"])

def read_stores(input_file:str,fieldnames:List) -> List[Dict]:
    with open(file = input_file, mode = 'r', encoding = 'utf-8', newline = '') as input:
        csvReader = csv.DictReader(input,fieldnames)
        next(csvReader,None) # skip header row
        results:List[Dict] = []
        for row in csvReader:
            results.append(row) # merge 2 dict
    return results

def write_csv_report(output_file:str,results: List[Dict]) -> None:
    """將轉換過的資料(results),寫入目標的csv檔(output_file)

    Args:
        results (List[Dict]): 地址轉換的列表
        output_file (str): 儲存的CSV路徑位址
    """
    with open(output_file, mode='w', encoding='utf-8', newline='') as csvfile:
        csvWriter = csv.DictWriter(csvfile,fieldnames=results[0].keys())
        csvWriter.writeheader()
        for result in results:
            csvWriter.writerow(result)
    pass

def create_output_file_name(output_folder:str,input_file_path:str,suffix:str) -> str:
    input_file_P = Path(input_file_path)
    output_folder_P = Path(output_folder)
    if(not input_file_P.is_file()):
        raise ValueError(f"Input file <{input_file_path}> is not a file.")
    # if(not input_file_P.suffix == suffix):
    #     raise ValueError(f'Input file <{input_file_path}> is not a {suffix} file')
    if(not output_folder_P.is_dir()):
        raise ValueError(f'Output folder <{output_folder}> is not a folder.')
    timestamp:str = datetime.strftime(datetime.now(tz=timezone.utc),"[%Y%m%d%z_%H'%M'%S]") # ex: "[20220412+0000_03'55'31]"
    return output_folder_P.joinpath(timestamp + input_file_P.stem).with_suffix(suffix).as_posix()

def get_APIKey_from_env()->str:
    """Try to load Geocoding API key in .env

    Raises:
        ValueError: Fail to read from environment.

    Returns:
        str: The API Key for web geocoding service.
    """
    load_dotenv()
    api_env_name:str = "BINGMAP_API_KEY"
    bing_api_key:str = os_getenv(api_env_name)
    if(bing_api_key is None):
        raise ValueError(f"Can't read API key with <{api_env_name}>, please check env file.")
    return bing_api_key

def main(input_file:str,output_folder:str) -> None:
    try:
        bing_api_key = get_APIKey_from_env()
        fieldnames = ["行政區","店名","地址","電話","坐標(緯度)","坐標(經度)"]
        stores:List[Dict] = read_stores(filepath,fieldnames)
        # --- 讀出店家資料後,將店家地址與轉換經緯度的結果整合,也可以考慮在這裡過濾錯誤的比對結果 ---
        results:List[Dict] = []
        for store in stores:
            r = geocoding.bing_address_geocoding(store["地址"],bing_api_key)
            print(f'Geocoding <{store["地址"]}>...')
            results.append(store|r)
        # --- 寫入一個csv檔,用來觀察geocoding 結果 ---
        output_csv_file:str = create_output_file_name(output_folder,input_file,'.csv')
        write_csv_report(output_csv_file,results)
        # --- 輸出KML ---
        placemarks:List[writekml.PlaceMark] = [convert_geocoding_result_to_palcemark(r) for r in results]
        kml = writekml.create_kml(points=placemarks)
        kml.save(create_output_file_name(output_folder,input_file,'.kml'))
        # --- 繪製地圖並開檔 ---
        markers:List[folium.Marker] = [ placemark_to_foluimMarker(p) for p in placemarks]
        map_path:str = create_output_file_name(output_folder,input_file,'.html')
        drawmap.draw_foluim_map(map_path,markers)
    except Exception as e:
        print(e)
    pass

if __name__ == '__main__':
    filepath:str = "testdata\嘉義市書店地圖.csv"
    output_folder:str = "testdata\output"
    main(filepath,output_folder)
    pass