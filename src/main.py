'''
## Describe

## Process

1. 讀取店家CSV資料
2. 將店家地址轉成經緯度儲存
3. 使用經緯度資訊與店家資訊,產生HTML地圖
4. (可選)輸出KML格式資料
5. 開啟地圖

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
- 
'''
#!/usr/bin/python3
import csv
from pathlib import Path
from decimal import Decimal
from typing import TypedDict,List,Dict
from os import getenv as os_getenv
from dotenv import load_dotenv # read api key from (.env) file 
from geocoder import bing as geocoder_bing

class GeocodingResult(TypedDict):
    """Define the function {bing_address_geocoding} return structure. This Structure also defines output file header.

    Args:
        house_address (str): Original address from source. ex: 
        Provider (str): API Provider. ex: "bing"
        Success (bool): Is api reply match.
        Lat (float): latitude. ex: None, 25.03360939025879
        Lng (float): longitude. ex: None, 121.56500244140625
        Match_address (str): ex: None, 'Taipei 101, Taiwan'
        Err_Message (str): Error mesage from api network reply. ex: 'ERROR - No results found', 'OK'
    """
    house_address:str 
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
        house_address = address,
        provider = reply.provider,
        success = reply.ok,
        lat = reply.lat,
        lng = reply.lng,
        match_address = reply.address,
        err_message = reply.status
    )

def process_file(input_file:str, output_file:str, api_key:str) -> None:
    """Open {input_file} to read house address, then call Bing map api transfer to latlng, save result to {output_file}.

    Warning: 
        - If you try to use big csv file for process, use other method like pandas framework.

    Args:
        input_file (str): _description_
        output_file (str): _description_
        api_key (str): _description_
    """
    with open(file = input_file, mode = 'r', encoding = 'utf-8', newline = '') as input, open(file = output_file, mode='w',encoding='utf-8', newline = '') as output:
        csvReader = csv.DictReader(input,fieldnames=["行政區","店名","地址","電話","坐標(緯度)","坐標(經度)"])
        next(csvReader,None) # skip header row
        csvWriter = csv.DictWriter(output,fieldnames=GeocodingResult.__annotations__.keys())
        csvWriter.writeheader()
        for row in csvReader:
            result:GeocodingResult = bing_address_geocoding(address = row["地址"],api_key=api_key)
            csvWriter.writerow(result)
            print(f"Process <{row['地址']}>.")
    pass

def geocoding_source_file(input_file:str, api_key:str) -> List[Dict]:
    results:List[GeocodingResult] = []
    with open(file = input_file, mode = 'r', encoding = 'utf-8', newline = '') as input:
        csvReader = csv.DictReader(input,fieldnames=["行政區","店名","地址","電話","坐標(緯度)","坐標(經度)"])
        next(csvReader,None) # skip header row
        for row in csvReader:
            result:GeocodingResult = bing_address_geocoding(address = row["地址"],api_key=api_key)
            results.append(result | row) # merge 2 dict
            print(f"Process <{row['地址']}>.")
    return results

def write_csv_report(results: List[Dict], output_file:str) -> None:
    with open(output_file, mode='w', encoding='utf-8', newline='') as csvfile:
        csvWriter = csv.DictWriter(csvfile,fieldnames=[])
        csvWriter.writeheader()
        for result in results:
            csvWriter.writerow(result)
    pass

def create_output_file_path(output_folder:str,input_file_path:str) -> str:
    """Combine the user defined output folder and data source to create new output file.

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
        output_file:str = create_output_file_path(output_folder,input_file)
        # process_file(input_file = input_file, output_file = output_file, api_key = bing_api_key)
        results = geocoding_source_file(input_file,bing_api_key)
        print(results)
    except Exception as e:
        print(e)
    pass

if __name__ == '__main__':
    filepath:str = "testdata\嘉義市書店地圖.csv"
    output_folder:str = "testdata\output"
    main(filepath,output_folder)
    pass