'''
input: 讀取店家資訊(.csv)
output: 根據店家地址寫入對應的經緯度資訊
'''
from dotenv import load_dotenv
import os
import geocoder 

class GeoCodeConverter():
    """
    A class to convert house address(String) to Geocode

    - Attribute:
        - api_provider:str # API服務提供者的名稱
        - api_key:str # 使用者提供的API key
        - batch_limit:(unsigned)int # API的批次轉換大小限制,每家API Provider的限制不同
    - Method:
        - GeoCoding()
        - BatchGeoCoding()
    """
    def __init__(self):
        self.api_provider:str = "Bing Map" # API服務
        self.api_key:str = ""
        pass

def add_longitude_to_CSV(csvfile:str,output:str) -> None:
    """
    1. 讀取API Key
    2. 讀取CSV檔的地址欄位
    3. 將地址欄位轉換成經緯度
        1. 如果正確，將經緯度存回新的欄位
        2. 如果找不到正確的經緯度 -> FIXTHIS
    """
    load_dotenv()
    key:str = os.getenv('BINGMAP_API_KEY')
    # get_BingMap_GeoCodeing(address="嘉義市西區600東區學府路300號",key=key)
    get_BingMap_GeoCodeing(address="嘉義市東區體育路29號",key=key)
    e = get_BingMap_GeoCodeing(address="搜尋所需地點",key=key,methods = 'batch')

    print(e)
    pass

'''
TODO:
- 輸入csv後,如何將輸出到新的資料規範化
'''