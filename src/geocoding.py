'''
負責將輸入的csv讀取轉換成準備輸出的格式
'''
import csv
from typing import TypedDict,List,Dict
from geocoder import bing as geocoder_bing

class GeocodingResult(TypedDict):
    """Define the function {bing_address_geocoding} return structure. This Structure also defines output file header.

    Describe:
        用來儲存地址轉經緯度後的資訊

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

    Ex:

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
    """Read the csv file(input_file), then turn store data into List[Dict]

    Ex:
    ``` python
    fieldnames = ["行政區","店名","地址","電話","坐標(緯度)","坐標(經度)"]
    results:List[Dict] = geocoding.geocoding_csv_file(input_file=filepath, api_key=bing_api_key, fieldnames=fieldnames, address_name="地址")
    ```

    ```
    [{'provider': 'bing', 'success': True, 'lat': 23.47914, 'lng': 120.44242, 'match_address': '583, Zhongshan Road, West District, Chiayi City 403', 'err_message': 'OK', '行政區': '西區', '店名': '墊腳石圖書文化廣場 嘉義店', '地址': '嘉義市西區中山路583號', '電話': '05-2273928', '坐標(緯度)': '23.4778754', '坐標(經度)': '120.4408611'},
{'provider': 'bing', 'success': True, 'lat': 23.48388, 'lng': 120.43251, 'match_address': '35, De-an Road, West District, Chiayi City 60085', 'err_message': 'OK', '行政區': '西區', '店名': '德安書局', '地址': '嘉義市西區德安路35號', '電話': '05-2338805', '坐標(緯度)': '23.4839524', '坐標(經度)': '120.4325974'}]
    ```

    Args:
        input_file (str): 資料來源的csv檔位置
        api_key (str): 給Bing map api使用
        fieldnames (List): 用來給csv.DictReader讀取資料欄位
        address_name (str): 定義資料欄位的地址欄位名稱

    Returns:
        List[Dict]: 一個組合了Geocoding查詢結果與原始資料的字典所組成的新列表
    """
    results:List[Dict] = []
    with open(file = input_file, mode = 'r', encoding = 'utf-8', newline = '') as input:
        csvReader = csv.DictReader(input,fieldnames)
        next(csvReader,None) # skip header row
        for row in csvReader:
            result:GeocodingResult = bing_address_geocoding(address=row[address_name], api_key=api_key)
            results.append(result|row) # merge 2 dict
            print(f"Process <{row[address_name]}>.")
    return results