'''
負責將輸入的csv讀取轉換成準備輸出的格式
'''

class GeocodingResult(TypedDict):
    """Define the function {bing_address_geocoding} return structure. This Structure also defines output file header.

    Describe:

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

def geocoding_source_file(input_file:str, api_key:str,fieldnames:List,address:str) -> List[Dict]:
    results:List[Dict] = []
    with open(file = input_file, mode = 'r', encoding = 'utf-8', newline = '') as input:
        csvReader = csv.DictReader(input,fieldnames)
        next(csvReader,None) # skip header row
        for row in csvReader:
            result:GeocodingResult = bing_address_geocoding(address,api_key=api_key)
            results.append(result|row) # merge 2 dict
            print(f"Process <{address}>.")
    return results