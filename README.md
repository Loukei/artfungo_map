# artfungo_map

## Describe

查詢並爬取藝fun劵商家(https://artsfungo.moc.gov.tw/promote_s/public/store)
將查詢的地址輸出成地圖

## Require modules:

- dotenv: https://pypi.org/project/python-dotenv/
- folium: https://python-visualization.github.io/folium/
- geocoder: https://geocoder.readthedocs.io/
- selenium: https://www.selenium.dev/
- Pandas: https://pandas.pydata.org/

## How to use

1. 安裝模組

2. 申請Bing map api(免費) https://www.bingmapsportal.com/ ,在專案資料夾建立一個.env文字檔
```
BINGMAP_API_KEY = "YOUR_KEY"
```

3. 下載selenium的[chrome webdriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)，注意版本與你的chrome瀏覽器對應，將chromedriver.exe放在專案資料夾

4. 執行craeler.py爬取藝fun卷資料，會將檔案存成data.csv

5. 執行aftfunmap.py會將data.csv轉為地圖(將地址轉為經緯度會花點時間)，之後打開map.html即可

## Work flow

1. 使用selenium開啟chrome瀏覽器，加載https://artsfungo.moc.gov.tw/promote_s/public/store
2. 輸入關鍵字，擷取商家名稱、地址等資訊
3. 透過geocoder將地址轉為經緯度並記錄下來(這裡使用bing map api)
4. 將步驟4的經緯度透過folium繪製在地圖上並標記
5. 將地圖離線保存
6. 用瀏覽器開啟地圖

## 開發筆記

這個專案是用來做python新手練習，開發大約花了兩個禮拜。
網路的時代多數的資訊都在網頁上，學會自動擷取資訊可以省下大量時間。
首先選擇folium與selenium作為開發使用的套件，因為他們都號稱易於使用。

### folium 建立地圖，保存

這裡應該沒有太多困難，location代表地圖中心點的經緯度(lat,lng)，zoom_start代表倍率，tiles代表使用的地圖供應商

``` python
import folium
fmap = folium.Map(location=map_center, zoom_start=16, tiles="OpenStreetMap")
```

保存地圖為html也只要一行

``` python
fmap.save('map.html')
```

同場加映，使用python開啟網頁，使用os模組轉成絕對路徑，再透過webbrowser開啟(使用者預設的瀏覽器)

``` python
import os
import webbrowser
abs_path = os.path.abspath(path)
webbrowser.open(abs_path)
```

- [folium:Getting Started](https://python-visualization.github.io/folium/quickstart.html#Getting-Started)
- [webbrowser --- 方便的Web浏览器控制器](https://docs.python.org/zh-cn/3/library/webbrowser.html)

### folium 添加marker

所謂marker就是指我們在google map上常見的紅色標記，將來要透過marker添加商家的訊息上去
location參數一樣是輸入(lat,lng)，tooltip代表滑鼠懸停的訊息，popup表示點擊後的資訊

``` python
folium.Marker(location=gcode,tooltip=shopname,popup=popup).add_to(map)
```

-[folium:Markers](https://python-visualization.github.io/folium/quickstart.html#Markers)

### geocoder轉換地址與地理位置

開發到這裡應該也察覺到了，繪製地圖需要將查詢地址轉為經緯度的服務。
查詢的服務每家的準確度都不同，以台灣來說使用TGOS或者Google map比較好。
TGOS為內政部提供的開放資料，而google map則是有真實的在台灣路上蒐集資訊。
TGOS沒有python的api，google map需要使用信用卡開通服務
我最後是使用bing map來做。

geocoder模組支援許多地圖服務商的地址轉換工具，包含google、mapbox、OpenstreetMap等。
參數address是查尋的地址，基本上附加國家名稱會更準確，key為api key的字串

``` python
latlng:tuple = geocoder.bing(address, key = os.getenv('BINGMAP_API_KEY')).latlng
```

-[Geocoder](https://geocoder.readthedocs.io/)

### 使用env檔管理api key

api key都是有限制流量的，你可以想像成每個人的手機通信費一樣，因此絕對不要公開個人開發用的api key
.env檔是一種純文字的格式，用來保存每個專案的環境變數，同時gitignore也不會同步env檔

``` python
from dotenv import load_dotenv
load_dotenv() # 從.env載入API key
key = os.getenv('BINGMAP_API_KEY')
```

.env檔內容

``` .env
BINGMAP_API_KEY = "YOUR API KEY"
```

-[python-dotenv](https://pypi.org/project/python-dotenv/)
-[Hiding API Keys with Environment Variables (dotenv) and Pushing Code to GitHub](https://www.youtube.com/watch?v=17UVejOw3zA)

### Selenium開啟網頁

作為爬蟲的入門，selenium是很適合新手的工具，特別是對網頁技術還不熟悉的使用者。
selenium會自動開啟瀏覽器執行網頁，點擊按鈕與連結，輸入字串到表單等，一切都在你眼前自動操作。
selenium的缺點最明顯的就是執行緩慢，瀏覽器本身就是記憶體怪獸，還要開啟之後才能進行操作，也沒有很好的針對ajax網頁爬取的方式。

```python
from selenium import webdriver
```

## 將取得的html原始碼存檔

``` python
with open('table.html','w',encoding='utf8') as file:
    file.write(getSearchResult(driver))
```

## Reference

[Selenium with Python中文翻译文档](https://selenium-python-zh.readthedocs.io/en/latest/index.html)

[Python爬蟲學習筆記(二) — Selenium自動化+Katalon Recorder](https://medium.com/@yanweiliu/python%E7%88%AC%E8%9F%B2%E5%AD%B8%E7%BF%92%E7%AD%86%E8%A8%98-%E4%BA%8C-selenium%E8%87%AA%E5%8B%95%E5%8C%96-ab0a27a94ff2)

[Selenium自動化測試：如何驗證網頁WebTable的值](https://www.qa-knowhow.com/?p=1930)

[透過 Selenium 操作下拉式選單 (Select)](https://jzchangmark.wordpress.com/2015/03/05/%E9%80%8F%E9%81%8E-selenium-%E6%93%8D%E4%BD%9C%E4%B8%8B%E6%8B%89%E5%BC%8F%E9%81%B8%E5%96%AE-select/)

[Python 3 筆記 - 自動安裝所需的 Module](https://mrnegativetw.github.io/Python-3-%E7%AD%86%E8%A8%98/Python3%E7%AD%86%E8%A8%98-%E8%87%AA%E5%8B%95%E5%AE%89%E8%A3%9D%E6%89%80%E9%9C%80%E7%9A%84Module/)

### 自動安裝selenium chome webdriver
[chromedriver-autoinstaller](https://pypi.org/project/chromedriver-autoinstaller/)

### 爬取table(s)
[Python selenium —— 一定要会用selenium的等待，三种等待方式解读](https://huilansame.github.io/huilansame.github.io/archivers/sleep-implicitlywait-wait)

[Waiting for a table to load completely using selenium with python](https://stackoverflow.com/questions/25221580/waiting-for-a-table-to-load-completely-using-selenium-with-python)

[Using Selenium with Python to parse table data](https://stackoverflow.com/questions/56607629/using-selenium-with-python-to-parse-table-data)

[How to recursively scrape table from pages using python selenium](https://stackoverflow.com/questions/57446861/how-to-recursively-scrape-table-from-pages-using-python-selenium)

[Waiting for a table to load completely using selenium with python](https://stackoverflow.com/questions/25221580/waiting-for-a-table-to-load-completely-using-selenium-with-python)

[Selenium学习（22）判断条件（1）](https://zhuanlan.zhihu.com/p/41396180)

### 
[Python 到底是 pass by value 還是 pass by reference? 一次搞懂程式語言的函式傳參!](http://dokelung.me/category/python/python-evaluation-strategy/)

### pandas datafram
[pandas入门](https://pda.readthedocs.io/en/latest/chp5.html)

[Add one row to pandas DataFrame](https://stackoverflow.com/questions/10715965/add-one-row-to-pandas-dataframe)

# AJAX處理
[Scrapy爬虫框架教程（四）-- 抓取AJAX异步加载网页](https://zhuanlan.zhihu.com/p/26257790)
[Requests: 让 HTTP 服务人类 快速上手](https://requests.readthedocs.io/zh_CN/latest/user/quickstart.html#module-requests.models)
