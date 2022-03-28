# artfungo_map

**<!> This repo is archived,since [artsfungo](https://artsfungo.moc.gov.tw) has closed**

## Describe

查詢並爬取藝fun劵商家(https://artsfungo.moc.gov.tw/promote_s/public/store)
將查詢的地址輸出成地圖

![Demo](https://github.com/Loukei/artfungo_map/blob/master/Demo.png?raw=true)

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
4. 將步驟3的經緯度透過`folium`繪製在地圖上並標記
5. 將地圖檔案保存
6. 用瀏覽器開啟地圖

## 開發筆記

這個專案是用來做python新手練習，開發大約花了兩個禮拜。

網路的時代多數的資訊都在網頁上，學會自動擷取資訊可以省下大量時間。

首先選擇`folium`與`selenium`作為開發使用的套件，因為他們都號稱易於使用。

### **folium 建立地圖，保存**

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

### **folium 添加marker**

所謂marker就是指我們在`google map`上常見的紅色標記，將來要透過marker添加商家的訊息上去。

location參數一樣是輸入(lat,lng)，tooltip代表滑鼠懸停的訊息，popup表示點擊後的資訊

``` python
folium.Marker(location=gcode,tooltip=shopname,popup=popup).add_to(map)
```

- [folium:Markers](https://python-visualization.github.io/folium/quickstart.html#Markers)

### **geocoder轉換地址與地理位置**

開發到這裡應該也察覺到了，繪製地圖需要將查詢地址轉為經緯度的服務。

查詢的服務每家的準確度都不同，以台灣來說使用`TGOS`或者`Google map`比較好。

`TGOS`為內政部提供的開放資料，而`google map`則是有真實的在台灣路上蒐集資訊。

TGOS沒有python的api，`google map`需要使用信用卡開通服務，我最後是使用bing map來做。

`geocoder`模組支援許多地圖服務商的地址轉換工具，包含`google`、`mapbox`、`OpenstreetMap`等。
參數address是查尋的地址，基本上附加國家名稱會更準確，key為api key的字串

``` python
latlng:tuple = geocoder.bing(address, key = os.getenv('BINGMAP_API_KEY')).latlng
```

- [Geocoder](https://geocoder.readthedocs.io/)

### **使用env檔管理api key**

api key都是有限制流量的，你可以想像成每個人的手機通信費一樣，因此絕對不要公開個人開發用的api key。

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

- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [Hiding API Keys with Environment Variables (dotenv) and Pushing Code to GitHub](https://www.youtube.com/watch?v=17UVejOw3zA)

### **Selenium開啟網頁**

作為爬蟲的入門，selenium是很適合新手的工具，特別是對網頁技術還不熟悉的使用者。
selenium會自動開啟瀏覽器執行網頁，點擊按鈕與連結，輸入字串到表單等，一切都在你眼前自動操作。
selenium的缺點最明顯的就是執行緩慢，瀏覽器本身就是記憶體怪獸，還要開啟之後才能進行操作，也沒有很好的針對ajax網頁爬取的方式。

selenium使用webdriver操作瀏覽器，webdriver是針對瀏覽器撰寫的驅動程式，需要上selenium網站進行下載符合你的瀏覽器版本。

第二行開啟了一個Chrome瀏覽器，參數指向webdriver的檔案地址
第三行開啟了藝fun卷的網站
注意在網站操作完畢後，使用`driver.close()`關閉driver

```python
from selenium import webdriver
driver = webdriver.Chrome('chromedriver.exe') # 開啟webdriver
driver.get('https://artsfungo.moc.gov.tw/promote_s/public/store') # 開啟藝fun卷:合作業者
```

- [Selenium](https://pypi.org/project/selenium/)
- [Selenium with Python中文翻译文档](https://selenium-python-zh.readthedocs.io/en/latest/index.html)
- [chromedriver-autoinstaller](https://pypi.org/project/chromedriver-autoinstaller/)
- [Python爬蟲學習筆記(二) — Selenium自動化+Katalon Recorder](https://medium.com/@yanweiliu/python%E7%88%AC%E8%9F%B2%E5%AD%B8%E7%BF%92%E7%AD%86%E8%A8%98-%E4%BA%8C-selenium%E8%87%AA%E5%8B%95%E5%8C%96-ab0a27a94ff2)

### **輸入關鍵字**

爬蟲的第一步是搜尋網頁中的元素進行操作，這需要使用者有一定的網頁設計知識。
selenium提供幾種不同搜尋的方法:

``` python
find_element_by_id 
find_element_by_name
find_element_by_xpath
find_element_by_link_text
find_element_by_partial_link_text
find_element_by_tag_name
find_element_by_class_name
find_element_by_css_selector
```

chrome瀏覽器提供的F12工具可以用滑鼠選擇網站上的元素，並取得XPATH或是css_selector來選擇元素。
藝fun卷網站上的網頁元素基本不提供id或name屬性，因此我偏向使用css_selector。

``` python
input_element = driver.find_element_by_css_selector('#div-result > input')
input_element.send_keys(query)
```

第一行透過driver取得當前網頁中的輸入框，回傳一個webelement。
利用webelement的`send_keys()`方法輸入搜尋字串，注意到如果抓到的元素不是input標籤，`send_keys()`方法不會生效。

### **按下搜尋按鈕**

藝fun卷網站不提供"輸入Enter"來搜尋的功能，因此需要按下旁邊的搜尋紐。
webelement使用`click()`方法按下按鈕。

``` python
search_element = driver.find_element_by_css_selector('#div-result > div > a')
search_element.click()
```

### **等待搜尋結果**

藝fun卷網站使用ajax技術，即網頁內容動態加載的方式，在按下搜尋鈕後不需要重新將整個網頁載入，而是發出特定的request等待server回傳資料，並更新下方的table元素。

因此，我們不能直接使用`find_element`方法，因為這樣撈到的網頁內容會是server尚未回傳之前的空資料。
有三種方法等待資料回傳

強制等待:使用python的`sleep()`方法

``` python
from time import sleep
sleep(3) # 強制等待3秒
```

隱式等待:如同while迴圈一般，隱式等待會在時間結束時搜尋對應元素，若沒有則進入下一個等待週期。

``` python
from selenium import webdriver

driver = webdriver.Firefox()
driver.implicitly_wait(10) # seconds
driver.get("http://somedomain/url_that_delays_loading")
myDynamicElement = driver.find_element_by_id("myDynamicElement")
```

顯式等待:

selenium會在特定的條件達成後立即執行下一步，同時限制最長等待時間
這也是我在這裡使用的方法，等待table > tbody > tr出現並收集所有出現的tr元素內容
下面的程式碼會等待最長7秒，如果出現(可見的狀態)tr元素則將所有tr收集起來並回傳list

``` python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    tbody_elements = WebDriverWait(driver,7).until(
        EC.visibility_of_all_elements_located((By.XPATH,'//*[@id="inpage"]/div/div/div[2]/div/table/tbody/tr'))
    )
    return tbody_elements
except:
    return []
```

- [Selenium with Python:Waits](https://selenium-python.readthedocs.io/waits.html)
- [Selenium自動化測試：如何驗證網頁WebTable的值](https://www.qa-knowhow.com/?p=1930)
- [Python selenium —— 一定要会用selenium的等待，三种等待方式解读](https://huilansame.github.io/huilansame.github.io/archivers/sleep-implicitlywait-wait)
- [Selenium学习（22）判断条件（1）](https://zhuanlan.zhihu.com/p/41396180)
- [Waiting for a table to load completely using selenium with python](https://stackoverflow.com/questions/25221580/waiting-for-a-table-to-load-completely-using-selenium-with-python)
- [Using Selenium with Python to parse table data](https://stackoverflow.com/questions/56607629/using-selenium-with-python-to-parse-table-data)
- [How to recursively scrape table from pages using python selenium](https://stackoverflow.com/questions/57446861/how-to-recursively-scrape-table-from-pages-using-python-selenium)
- [Waiting for a table to load completely using selenium with python](https://stackoverflow.com/questions/25221580/waiting-for-a-table-to-load-completely-using-selenium-with-python)

### **取得table元素的頁數**

藝fun卷的網頁在查詢之前是不會顯示tfoot元素，也就是頁碼，直到查詢之後才能得知搜索結果有幾頁。
因此此項作業必須在第一頁出現之後才能取得。

仔細觀察網頁原始碼，你可以注意到tfoot分成"最前頁""上一頁""1""2""3""下一頁""最末頁"
我在這裡直接撈取`<ul class = 'pagination'>`的內部元素列表然後-4

``` python
# 從tfoot元素移動到內部的class = pagination元素，這個list保存所有分頁連結
pagination = driver.find_element_by_css_selector('#inpage > div > div > div.rim > div > table > tfoot > tr > td > nav > ul')
# 搜尋page-item的list
pageitems = pagination.find_elements_by_class_name('page-item')
# 搜尋到的list會多出4個(最前頁,上一頁,下一頁,最後頁)
return len(pageitems) - 4
```

### **解析與取得網頁內容**

selenium的webelement提供取得網頁屬性的方法

下面的程式碼會取得網頁的table元素(透過css selector)，接著透過`innerHTML`屬性取得table的html程式碼

``` python
table_element = driver.find_element_by_css_selector('#inpage > div > div > div.rim > div > table')
htmlcontent:str = table_element.get_attribute('innerHTML')
```

下面的程式碼針對table的tr元素撈取文字內容，分別取得'店名'、'地址'、'電話號碼'、'藝文類型'

```
table > thead
      > tbody > tr > td '網址'
                   > td '店名'
                   > td '地址'
                   > td '電話號碼'
                   > td '藝文類型'
              > tr
```

``` python
input['店名'].append(row.find_element_by_xpath('./td[2]').text)
input['地址'].append(row.find_element_by_xpath('./td[3]').text)
input['電話號碼'].append(row.find_element_by_xpath('./td[4]').text) 
input['藝文類型'].append(row.find_element_by_xpath('./td[5]').text)
```

### **Pandas**

Pandas是一個資料處理的框架，提供使用者處理表格資料。

Pandas也可以撈取html的table，但是並不會過濾內容()。

``` python
import pandas as pd
#only 1 dataframe in single page
df:pd.core.frame.DataFrame = pd.read_html(driver.page_source)[0]
```

Pandas的表格操作使用DataFrame，最簡單的方式是使用一個空的字典，欄位名稱使用字串定義，value則使用list表示各項內容

``` python
# 建立一個空的DataFrame
result = pd.DataFrame({ "店名": [],"地址": [],"電話號碼": [],"藝文類型":[] })
```

針對表格的每一列可以使用`append()`添加列，或者你可以使用list事先收集所有內容再對DataFrame初始化

``` python
row = {"店名": "嘉大咖啡學園","地址": "嘉義市西區600東區學府路300號","電話號碼": "05-276-1601","藝文類型":"地方文化館"}
result = result.append(row,ignore_index=True)
```

有了這些就可以迭代取出table元素裡的每一頁內容並填入DataFrame

### **將DataFrame輸出成csv檔**

將爬取到的內容儲存成csv檔，減少執行爬蟲消耗的時間

``` python
result.to_csv('data.csv')
```

### **將取得的html原始碼存檔**

``` python
with open('table.html','w',encoding='utf8') as file:
    file.write(getSearchResult(driver))
```

## 結語&可以改進之處

**效率不高**

可以發現使用`selenium`爬取資料相當花費時間，它本身做自動化而非設計來爬蟲的框架，開啟瀏覽器不僅耗時且花費記憶體，也無法針對ajax的部分做良好的處理，像是要爬取搜尋第二頁的內容，因為table內部本身已經有第一頁的資料，除非紀錄並比對內容差異，否則程式無法知道第二頁以後內容是否更新。

另一個問題是我沒有採取`async`的方式，在將地址轉為經緯度值的時候都需要等待server回傳才能執行下一個動作。

最後，我是使用爬取店家資訊 > 查詢地理位址 > 建立marker 的順序依序執行三個迴圈來操作，如果把三件事情用一個迴圈做完可以跑的更快。

**UI問題**

folium的存檔功能還是要上網才能看到地圖，無法完全離線使用，這樣子比起手機APP還難用。
另一個是店家的資訊比較多的情況下，使用網頁的list連動marker會比較好，就像是`google map`一樣。

**離線地圖的解決方式**

1. 自架一個本地Server來提供圖層(tiles)
   1. [Host Your Own Offline Mapping Server with Jupyter Notebook](https://towardsdatascience.com/host-your-own-offline-mapping-server-with-jupyter-notebook-ff21b878b4d7)

2. 將儲存的商家資料地理標記儲存成KML(Keyhole Markup Language)格式
   1. 通過[Google我的地圖](https://www.google.com.tw/intl/zh-TW/maps/about/mymaps/)來匯入KML地理標記，可以在手機APP上開啟，並且使用者可以離線下載來使用，應該會是最適合一般使用者的方案。
   2. KML是公開的格式，因此其他的離線地圖APP如[MAPS.ME](https://play.google.com/store/apps/details?id=com.mapswithme.maps.pro&hl=zh_TW&gl=US)也可以匯入使用。

## Reference

- [透過 Selenium 操作下拉式選單 (Select)](https://jzchangmark.wordpress.com/2015/03/05/%E9%80%8F%E9%81%8E-selenium-%E6%93%8D%E4%BD%9C%E4%B8%8B%E6%8B%89%E5%BC%8F%E9%81%B8%E5%96%AE-select/)

- [Python 3 筆記 - 自動安裝所需的 Module](https://mrnegativetw.github.io/Python-3-%E7%AD%86%E8%A8%98/Python3%E7%AD%86%E8%A8%98-%E8%87%AA%E5%8B%95%E5%AE%89%E8%A3%9D%E6%89%80%E9%9C%80%E7%9A%84Module/)

### python 傳參機制

- [Python 到底是 pass by value 還是 pass by reference? 一次搞懂程式語言的函式傳參!](http://dokelung.me/category/python/python-evaluation-strategy/)

### pandas datafram

- [pandas入门](https://pda.readthedocs.io/en/latest/chp5.html)

- [Add one row to pandas DataFrame](https://stackoverflow.com/questions/10715965/add-one-row-to-pandas-dataframe)

### AJAX處理

- [Scrapy爬虫框架教程（四）-- 抓取AJAX异步加载网页](https://zhuanlan.zhihu.com/p/26257790)
- [Requests: 让 HTTP 服务人类 快速上手](https://requests.readthedocs.io/zh_CN/latest/user/quickstart.html#module-requests.models)
