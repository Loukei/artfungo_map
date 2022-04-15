'''
## Describe

## Process

1. 讀取店家CSV資料
2. 將店家地址轉成經緯度儲存
3. 使用經緯度資訊與店家資訊,產生HTML地圖
4. 開啟地圖
5. (可選)輸出KML格式資料

## Usage

- Create a `.env` file which include "BINGMAP_API_KEY = YOUR_API_KEY"
- 

## Note

以我使用Bing Map的經驗, batch geocoding是較不推薦的方式
- 回應時間較長
- 只會回傳經緯度數值,不會有錯誤訊息與比對狀態

## TODO

- 利用裝飾子模式修整輸入與輸出流程
    - 裝飾子能巢狀嗎?
- 處理大型檔案時這種方式不適用
- 用Decimal來存經緯度
'''
#!/usr/bin/python3
import csv
from pathlib import Path
from decimal import Decimal
from pyclbr import Function
from typing import TypedDict,List,Dict
from os import getenv as os_getenv
from dotenv import load_dotenv # read api key from (.env) file 
from geocoder import bing as geocoder_bing
from drawmap import Store,write_foluim_map,create_output_map_path,test_locations

class GeocodingResult(TypedDict):
    """Define the function {bing_address_geocoding} return structure. This Structure also defines output file header.

    Args:
        Provider (str): API Provider. ex: "bing"
        Success (bool): Is api reply match.
        Lat (float): latitude. ex: None, 25.03360939025879
        Lng (float): longitude. ex: None, 121.56500244140625
        Match_address (str): ex: None, 'Taipei 101, Taiwan'
        Err_Message (str): Error mesage from api network reply. ex: 'ERROR - No results found', 'OK'
    """
    provider:str
    success:bool
    lat:float
    lng:float
    match_address:str
    err_message:str

def bing_address_geocoding(address:str,api_key:str) -> GeocodingResult:
    """Turn house {address} to geocode and show other debug message.

    Args:
        address (str): House address, ex: "台北101"
        api_key (str): API key for Bing Map Geocoding service

    Returns:
        GeocodingResult: The Geocoding information result.
    """
    reply = geocoder_bing(address, key = api_key)
    return GeocodingResult(
        provider = reply.provider,
        success = reply.ok,
        lat = reply.lat,
        lng = reply.lng,
        match_address = reply.address,
        err_message = reply.status
    )

def geocoding_csv_file(input_file:str, api_key:str,fieldnames:List,address_name:str) -> List[Dict]:
    results:List[Dict] = []
    with open(file = input_file, mode = 'r', encoding = 'utf-8', newline = '') as input:
        csvReader = csv.DictReader(input,fieldnames)
        next(csvReader,None) # skip header row
        for row in csvReader:
            result:GeocodingResult = bing_address_geocoding(address=row[address_name], api_key=api_key)
            results.append(result|row) # merge 2 dict
            print(f"Process <{row[address_name]}>.")
    return results

def write_csv_report(results: List[Dict], output_file:str) -> None:
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

def create_output_csv_file_path(output_folder:str,input_file_path:str) -> str:
    """Combine the user defined output folder and data source to create new output file.
    
    Ex:
        ``` python
        s = create_output_csv_file_path("C:\Documents\results","C:\Documents\Store.csv")
        # 'C:\Documents\results\Result_Store.csv'
        ```
    Args:
        output_folder (str): A folder path. ex: 'C:\Documents\results'
        input_file_path (str):A file path(csv), which include the house addresses. ex: "C:\Documents\Store.csv"

    Raises:
        ValueError: 

    Returns:
        str: A file path which is not yet created. ex: 'C:\Documents\results\Result_Store.csv'
    """
    output_dir:Path = Path(output_folder)
    input_file_path:Path = Path(input_file_path)
    if(not output_dir.is_dir()):
        raise ValueError(f'Args output_folder = <{output_folder}> is not an exist folder.')
    output_file_name:str = "Result_" + input_file_path.name
    return output_dir.joinpath(output_file_name)

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
        # results:List[Dict] = geocoding_source_file(input_file,bing_api_key)
        # --- 修改讀檔的模式,盡量讓隨著檔案變化的部分保留在最外層 ---
        fieldnames = ["行政區","店名","地址","電話","坐標(緯度)","坐標(經度)"]
        results:List[Dict] = geocoding_csv_file(input_file=filepath, api_key=bing_api_key, fieldnames=fieldnames, address_name="地址")
        
        output_csv_file:str = create_output_csv_file_path(output_folder,input_file)
        write_csv_report(results,output_csv_file)
        # --- 準備填入地圖的數據 ---
        # stores:List[Store] = []
        # for r in results:
        #     s = Store(name=r["店名"],address=r["地址"],lat=float(r["坐標(緯度)"]),lng=float(r["坐標(經度)"]),phone_number=r["電話"])
        #     stores.append(s)
        # --- 繪製地圖並開檔 ---
        # map_path:str = create_output_map_path(input_file,output_folder)
        # write_foluim_map(map_path,stores)
        # --- TODO KML 處理 ---
    except Exception as e:
        print(e)
    pass

if __name__ == '__main__':
    filepath:str = "testdata\嘉義市書店地圖.csv"
    output_folder:str = "testdata\output"
    main(filepath,output_folder)
    # ---
    # bing_api_key = get_APIKey_from_env()
    # fieldnames = ["行政區","店名","地址","電話","坐標(緯度)","坐標(經度)"]
    # results = geocoding_csv_file(input_file=filepath, api_key=bing_api_key, fieldnames=fieldnames, address_name="地址")
    # for row in results:
    #     print(row)
    pass