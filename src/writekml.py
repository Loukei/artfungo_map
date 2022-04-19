""" 提供一個方便的函數來讓店家資料轉成kml格式

## kml格式

### placemark 地標

- name 
- description: 說明文字
- Point: 經緯度

## Example

``` Python
import simplekml

if __name__ == "__main__":
    kml = simplekml.Kml()
    kml.newpoint(name="Kirstenbosch", coords=[(18.432314,-33.988862)])  # lon, lat, optional height
    kml.save("botanicalgarden.kml")
```

## Reference

kml 模組
- [simplekml](https://simplekml.readthedocs.io/en/latest/gettingstarted.html#quick-example)
- [kml格式說明](https://sammystuart.blog/kml-in-google-my-maps/)
"""
import simplekml
from typing import List,TypedDict

class PlaceMark(TypedDict):
    name: str       # 地標(店家)名稱
    describe: str   # 詳細的說明,如地址,電話,評論...
    lat:float       # 緯度 [-90.0 ~ 90.0]
    lng:float       # 經度 [-180.0 ~ 180.0]

def create_kml(points:List[PlaceMark]):
    kml = simplekml.Kml()
    p:PlaceMark
    for p in points:
        kml.newpoint(name= p["name"], description = p["describe"], coords=[(p["lng"],p["lat"])])
    return kml