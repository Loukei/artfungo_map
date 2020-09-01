# artfungo_map

## Describe

查詢並爬取藝fun劵商家(https://artsfungo.moc.gov.tw/promote_s/public/store)
將查詢的地址輸出成離線地圖

## Require modules:

- dotenv: https://pypi.org/project/python-dotenv/
- folium: https://python-visualization.github.io/folium/
- geocoder: https://geocoder.readthedocs.io/
- selenium: https://www.selenium.dev/

## How to use

1. 安裝模組

2. 申請Bing map api(免費) https://www.bingmapsportal.com/ ,在專案資料夾建立一個.env文字檔
```
BINGMAP_API_KEY = "YOUR_KEY"
```

3. 下載selenium的[chrome webdriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)，注意版本與你的chrome瀏覽器對應，將webdriver放在專案資料夾

4. 執行程式

## Work flow

1. 使用selenium開啟chrome瀏覽器，加載https://artsfungo.moc.gov.tw/promote_s/public/store
2. 輸入關鍵字，等待搜尋結果出現
3. 擷取商家名稱、地址等資訊
4. 透過geocoder將地址轉為經緯度並記錄下來(這裡使用bing map api)
5. 將步驟4的經緯度透過folium繪製在地圖上並標記
6. 將地圖離線保存
7. 用瀏覽器開啟地圖

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

24.96000 121.24000

24.96654、121.26114
24.95687、121.22609