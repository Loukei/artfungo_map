""" 提供一個方便的函數來讓店家資料轉成kml格式

## kml格式

### placemark 地標

- name 
- description: 說明文字
- Point: 經緯度

https://simplekml.readthedocs.io/en/latest/geometries.html#simplekml.Point

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
from typing import List
import placemark

def create_kml(points:List[placemark.PlaceMark]) -> simplekml.kml.kml:
    kml:simplekml.kml.kml = simplekml.Kml()
    p:placemark.PlaceMark
    for p in points:
        kml.newpoint(name= p["name"], description = p["describe"], coords=[(p["lat"],p["lng"])])
    return kml

if __name__ == "__main__":
    kml:simplekml.kml.kml = simplekml.Kml()
    # kml.newpoint(name="Kirstenbosch", description = "{house_address},{phone_number}", coords=[(18.432314,-33.988862)])  # lon, lat, optional height
    kml.newpoint()
    kml.save("botanicalgarden.kml")