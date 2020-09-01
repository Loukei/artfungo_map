'''
使用者指定關鍵字，利用爬蟲擷取藝fun卷商家資訊，並繪製成地圖後儲存成html
'''
import pandas as Pandas
import os
from dotenv import load_dotenv
import folium   # 繪製並存取地圖 https://python-visualization.github.io/folium/
import geocoder # 將地址轉為經緯度 https://geocoder.readthedocs.io/index.html
import webbrowser

def latlngBound(box:list,latlng:tuple) ->list:
    '''
    將一個bounding box與一個坐標系latlng計算，回傳新的bounding box
    [(-90.0,-180.0),(90.0,180.0)]
    '''
    lat:float = latlng[0]
    lng:float = latlng[1]
    latMin:float = lat if lat < box[0][0] else box[0][0]
    lngMin:float = lng if lng < box[0][1] else box[0][1]
    latMax:float = lat if lat > box[1][0] else box[1][0]
    lngMax:float = lng if lng > box[1][1] else box[1][1]
    return [(latMin,lngMin),(latMax,lngMax)]

def getBoundingBoxCenter(box:list,ndigits: int) -> tuple:
    lat = round( (box[1][0] - box[0][0]) / 2 , ndigits) # (lat_max - lat_min)/2 取至第ndigits位
    lng = round((box[1][1] - box[0][1]) / 2 , ndigits) # (lng_max - lng_min)/2
    return (lat,lng)

def openFileOnBrowser(path:str) -> None:
    abs_path = os.path.abspath(path)
    print(f'開啟地圖:{abs_path}')
    webbrowser.open(abs_path)

data = Pandas.read_csv('data.csv')
load_dotenv() # 載入 .env

# 將地址轉為geocode，同時計算Bounding box
latlng_list:list = []
bBox = [(90.0,180.0),(-90.0,-180.0)] # 初始值為與[最大座標,最小座標]
for i in range(len(data.index)): # 
    address:str = data.iloc[i]['地址']
    latlng:tuple = geocoder.bing(address, key = os.getenv('BINGMAP_API_KEY')).latlng
    if not latlng:
        continue
    else:
        latlng_list.append(latlng)
        bBox = latlngBound(bBox,latlng)

# 由bounding box計算地理中心點
print(bBox)
map_center = getBoundingBoxCenter(bBox,5)
print(map_center)
# 以地理中心繪製地圖
fmap = folium.Map(location=map_center, zoom_start=16, tiles="OpenStreetMap")
fmap.fit_bounds(bBox)
# 保存地圖
filePath :str = 'map.html'
fmap.save(filePath)
# Open webbrowser to show result
openFileOnBrowser(filePath)

os.system('PAUSE')
