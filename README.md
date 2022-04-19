# artfungo_map

**<!> This repo is archived,since [artsfungo](https://artsfungo.moc.gov.tw) has closed**

- 對輸出的地圖有興趣? 
  - 這裡重新使用了開放資料，讓你可以比對轉換後的經緯度
  - [原始碼](https://github.com/Loukei/artfungo_map/blob/master/src/main.py)
  - [嘉義市書店地圖](https://github.com/Loukei/artfungo_map/blob/master/testdata/%E5%98%89%E7%BE%A9%E5%B8%82%E6%9B%B8%E5%BA%97%E5%9C%B0%E5%9C%96.csv) : 原始資料
  - [嘉義市書店地圖.csv](https://github.com/Loukei/artfungo_map/blob/master/testdata/output/%5B20220419%2B0000_01'25'59%5D%E5%98%89%E7%BE%A9%E5%B8%82%E6%9B%B8%E5%BA%97%E5%9C%B0%E5%9C%96.csv): 轉換後的csv報告
  - [嘉義市書店地圖.kml](https://github.com/Loukei/artfungo_map/blob/master/testdata/output/%5B20220419%2B0000_01'25'59%5D%E5%98%89%E7%BE%A9%E5%B8%82%E6%9B%B8%E5%BA%97%E5%9C%B0%E5%9C%96.kml): kml格式可以更方便離線使用
  - [嘉義市書店地圖.html](https://github.com/Loukei/artfungo_map/blob/master/testdata/output/%5B20220419%2B0000_01'25'59%5D%E5%98%89%E7%BE%A9%E5%B8%82%E6%9B%B8%E5%BA%97%E5%9C%B0%E5%9C%96.html)

## Describe

查詢並爬取藝fun劵商家(https://artsfungo.moc.gov.tw/promote_s/public/store)
將查詢的地址輸出成地圖

![Demo](https://github.com/Loukei/artfungo_map/blob/master/Demo.png?raw=true)

## Require modules:

- [dotenv](https://pypi.org/project/python-dotenv/)
- [folium](https://python-visualization.github.io/folium/)
- [geocoder](https://geocoder.readthedocs.io/)
- [selenium](https://www.selenium.dev/)
- [Pandas](https://pandas.pydata.org/)
- [simplekml](https://simplekml.readthedocs.io/en/latest/)

## How to use

1. 下載專案
2. 安裝模組`pipenv install`
3. 申請[Bing map api(免費)](https://www.bingmapsportal.com/) 
   1. 在專案資料夾建立一個`.env`文字檔

```
BINGMAP_API_KEY = "YOUR_KEY"
```

3. 下載`selenium`的[chrome webdriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)，注意版本與你的chrome瀏覽器對應，將`chromedriver.exe`放在專案資料夾
   1. 可以利用[Webdriver Manager for Python](https://github.com/SergeyPirogov/webdriver_manager)來管理webdriver
4. 執行`crawler.py`爬取藝fun卷資料，會將檔案存成`data.csv`
5. 執行`aftfunmap.py`會將data.csv轉為地圖(將地址轉為經緯度會花點時間)，之後打開`map.html`即可

## Work flow

1. 使用`selenium`開啟`chrome`瀏覽器，加載[地址](https://artsfungo.moc.gov.tw/promote_s/public/store)
2. 輸入關鍵字，擷取商家名稱、地址等資訊
3. 透過`geocoder`將地址轉為經緯度並記錄下來(這裡使用bing map api)
4. 將**步驟3**的經緯度透過`folium`繪製在地圖上並標記
5. 將地圖檔案保存
6. 用瀏覽器開啟地圖

## 開發筆記

[傳送門](https://github.com/Loukei/artfungo_map/blob/master/Doc/%E9%96%8B%E7%99%BC%E7%AD%86%E8%A8%98.md)

## 後記

### 效率

- Selenium 可以用來處理AJAX的請求，因此一些動態渲染的資料可以在瀏覽器上渲染出來之後經由Selenium抓下來，不用開發者手動去解析封包或JS程式碼
- 壞處就是這樣做比較耗資源
- Selenium需要根據每個環境下載webdriver
  - 有一個開源工具[Webdriver Manager for Python](https://github.com/SergeyPirogov/webdriver_manager)可以處理webdriver的版本
  - 或者把爬蟲放在Docker部屬來解決

### 離線地圖

- `folium`模組幫開發者減少了撰寫地圖的工作,其內部就是使用模版把html畫出來
- 但是畫出來的地圖仍然需要聯網來取得map tile
- 比較方便的做法是直接輸出`KML`格式，接著透過Google我的地圖或是`MAPS.ME`匯入我們的店家資料

## Reference

- [開放政府- 嘉義市書店地圖](https://data.gov.tw/dataset/82835)
