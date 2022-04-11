# coding=utf-8
'''
## Describe

將地址轉經緯度的部分包裝起來,保留修改空間(更改供應商,使用其他的Geocoding模組)

## Change Geocode Provider

1. Write a function to fill the GeoCodingParameters
2. Write a function use GeoCodingParameters as parameter, than return latlng as result

## Exmple

```
params:GeoCodingParameters = BuildBingMapParameters()
result:Dict = bing_geocoding(address='台北101', api_key=params.api_key)
print(e)
```

## TODO:
- 考慮以後用工廠模式來裝配`GeoCodingParameters`
'''
from dataclasses import dataclass
from typing import List, Tuple
from os import getenv
from dotenv import load_dotenv # read api key from (.env) file 
import geocoder

@dataclass
class GeoCodingParameters:
    """A data container type to store API data

    Attributes:
        api_provider: The name for Geocoding web service, ex: "Google Map", "Bing Map", "TGOS".
        api_batch_limit: The limit number for batch geocoding, ex: "Bing Map" limit is 50.
        api_key: The API key string to access geocoding service.
    """    
    api_provider: str
    api_batch_limit: int
    api_key:str

@dataclass
class GeoCodeReply:
    """將回傳結果包裝起來,只儲存我們感興趣的資訊

    Attributes:
        provider:   網路服務供應者的名稱, ex: "bing", "google"
        sucess:     請求是否成功? ex: False,True
        latlng:     經緯度數值  ex: (None,None), (25.033609,121.565002)
        address:    比對到的第一個地址(英文),用來表示供應者認為的地址 ex: None, 'Taipei 101, Taiwan'
        err_msg:    失敗的原因描述 ex: 'ERROR - No results found', 'OK'
    """    
    provider:str
    sucess:bool
    latlng: Tuple[float,float]
    address:str
    err_msg:str

def BuildBingMapParameters()->GeoCodingParameters:
    """Return the Bing Map GeoCoding Parameter by hardcode.

    Read api_key from .env file

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        GeoCodingParameters: _description_
    """     
    if(load_dotenv() == False):
        raise ValueError('Loading env error.')
    api_key = getenv("BINGMAP_API_KEY")
    if(api_key == ""):
        raise ValueError("Can't read API key [BINGMAP_API_KEY] in env.")
    return GeoCodingParameters(api_provider="Bing Map", api_batch_limit=50, api_key=api_key)

def bing_geocoding(address:str, api_key:str) -> GeoCodeReply:
    """Call geocoder.bing() to get geocode, then package to GeoCodeReply

    Args:
        address (str): House address for geocoding
        api_key (str): API key for Bing map geocoding service

    Returns:
        GeoCodeReply: _description_
    """    
    reply = geocoder.bing(address, key = api_key)
    return GeoCodeReply(
        provider = reply.provider,
        sucess = reply.ok,
        latlng = tuple(reply.latlng),
        address = reply.address,
        err_msg = reply.status
    )

def bing_batch_geocoding(addres_list:List[str], api_key:str):
    reply = geocoder.bing(addres_list, key = api_key)
    pass

params:GeoCodingParameters = BuildBingMapParameters()
# ans = bing_geocoding(address='鐢辨湀瑕佸ソ濂藉涔犲ぉ澶╁悜涓?', api_key=params.api_key)
ans = bing_geocoding(address='台北101', api_key=params.api_key)
print(ans)
