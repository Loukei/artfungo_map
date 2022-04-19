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
    - 撰寫一個函數`convert_geocoding_result_to_palcemark()`
        - 將輸出的報告`results`轉換成`writekml.PlaceMark`,紀錄(經度,緯度,店名,詳細資訊)

## Note

以我使用Bing Map的經驗, batch geocoding是較不推薦的方式
- 回應時間較長
- 只會回傳經緯度數值,不會有錯誤訊息與比對結果
- 處理大型檔案時這種方式不適用

為何要輸出csv報告
- Geocoding的部分涉及了語意分析,你可以輸入一個明顯錯誤的地址,但卻得到"OK",這部分可能需要人工判讀
'''

#!/usr/bin/python3
from typing import List,Dict
from os import getenv as os_getenv
from dotenv import load_dotenv # read api key from (.env) file 
from myutils import read_stores,write_csv_report,create_output_file_name
import geocoding
import writekml
import folium 
import drawmap

def convert_geocoding_result_to_palcemark(result:Dict) -> writekml.PlaceMark:
    """將地址轉經緯度的報告{result}轉成PlaceMark格式

    Detail:
        PlaceMark主要用來儲存三個訊息: 經緯度(lat,lng),地標名稱(name),詳細描述(describe)
        不管在輸出kml或folium地圖所需的參數就只需這三個,但是使用者必須根據來源的csv格式親自處理這些轉換

    Args:
        result (Dict): 經緯度轉換過後的資料,通常會同時包含
            (店名,地址,電話): 原始檔案資料
            (Provider,Success,Lat,Lng,Match_address,Err_Message): 地址轉換經緯度後的紀錄

    Returns:
        writekml.PlaceMark: 包含地點資訊的字典 ex: {"name":"","describe":"","lat":0.0,"lng":0.0}
    """
    describe:str = f'Name: {result["店名"]}, Address: {result["地址"]}, Phone_number: {result["電話"]}'
    return writekml.PlaceMark(name=result["店名"],describe=describe,lat=result["lat"],lng=result["lng"])

def placemark_to_foluimMarker(placemark:writekml.PlaceMark) -> folium.Marker:
    return folium.Marker(location=[placemark["lat"],placemark["lng"]],popup=placemark["describe"],tooltip=placemark["name"])

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
        # --- 讀出店家資料後,將店家地址與轉換經緯度的結果整合,使用者也可以考慮在這裡過濾錯誤的比對結果 ---
        results:List[Dict] = []
        for store in stores:
            print(f'Geocoding <{store["地址"]}>...')
            r = geocoding.bing_address_geocoding(store["地址"],bing_api_key)
            results.append(store|r) #combine 2 dict
        # --- 寫入一個csv檔,用來觀察geocoding 結果 ---
        output_csv_file:str = create_output_file_name(output_folder,input_file,'.csv')
        write_csv_report(output_csv_file,results)
        # --- 輸出KML ---
        placemarks:List[writekml.PlaceMark] = [convert_geocoding_result_to_palcemark(r) for r in results]
        kml = writekml.create_kml(points=placemarks)
        kml.save(create_output_file_name(output_folder,input_file,'.kml'))
        # --- 繪製地圖並開檔 ---
        markers:List[folium.Marker] = [placemark_to_foluimMarker(p) for p in placemarks]
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