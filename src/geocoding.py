'''
## Describe

將地址轉經緯度的部分包起來,以後要修改時(比如改用Google map)只需改動這裡

## Usage

呼叫`geocoding_csv_file()`即可,會回傳一個字典{GeocodingResult}

'''
from typing import TypedDict
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
