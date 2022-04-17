from typing import Dict,TypedDict

class PlaceMark(TypedDict):
    name: str       # 地標(店家)名稱
    describe: str   # 詳細的說明,如地址,電話,評論...
    lat:float
    lng:float
