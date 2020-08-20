# artfungo_map

## Describe

查詢並爬取藝fun劵商家(https://artsfungo.moc.gov.tw/promote_s/public/store)
將查詢的地址輸出成離線地圖

## Require modules:

- folium
- geocoder
- selenium

## How to use

## Work flow

1. 使用selenium開啟chrome瀏覽器，加載https://artsfungo.moc.gov.tw/promote_s/public/store
2. 輸入關鍵字，等待搜尋結果出現
3. 擷取商家名稱、地址等資訊
4. 透過geocoder將地址轉為經緯度並記錄下來(這裡使用bing map api)
5. 將步驟4的經緯度透過folium繪製在地圖上並標記
6. 將地圖離線保存
7. 用瀏覽器開啟地圖

## Reference

[Selenium with Python中文翻译文档](https://selenium-python-zh.readthedocs.io/en/latest/index.html)

[Python爬蟲學習筆記(二) — Selenium自動化+Katalon Recorder](https://medium.com/@yanweiliu/python%E7%88%AC%E8%9F%B2%E5%AD%B8%E7%BF%92%E7%AD%86%E8%A8%98-%E4%BA%8C-selenium%E8%87%AA%E5%8B%95%E5%8C%96-ab0a27a94ff2)

[Using Selenium with Python to parse table data](https://stackoverflow.com/questions/56607629/using-selenium-with-python-to-parse-table-data)

[Selenium自動化測試：如何驗證網頁WebTable的值](https://www.qa-knowhow.com/?p=1930)

[透過 Selenium 操作下拉式選單 (Select)](https://jzchangmark.wordpress.com/2015/03/05/%E9%80%8F%E9%81%8E-selenium-%E6%93%8D%E4%BD%9C%E4%B8%8B%E6%8B%89%E5%BC%8F%E9%81%B8%E5%96%AE-select/)
