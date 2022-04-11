"""
使用selenium爬蟲擷取藝fun卷網站合作店家資料,輸出地址與店名
"""
from selenium import webdriver
import sys
import os
import pandas as pd
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def setQueryString(driver:webdriver,query:str) -> None:
    "輸入關鍵字"
    input_element = driver.find_element_by_css_selector('#div-result > input')
    input_element.send_keys(query)

def clickSearchBtn(driver:webdriver) -> None:
    "按下搜尋按鈕"
    search_element = driver.find_element_by_css_selector('#div-result > div > a')
    search_element.click()

def waitForSearchResult(driver:webdriver,max_wait:int) -> list:
    "等待搜尋結果，回傳WebElement list" # BUG 這個方法是檢查table內容是否出現，而非是否更新
    try:
        tbody_elements = WebDriverWait(driver,max_wait).until(
            EC.visibility_of_all_elements_located((By.XPATH,'//*[@id="inpage"]/div/div/div[2]/div/table/tbody/tr'))
        )
        return tbody_elements
    except:
        return []

def waitForSearchUpdate(driver:webdriver,wait:float) -> list:
    "等待搜尋頁面更新完成"
    # 取出上一頁的最後一個店名作為識別符號(lastShop)
    # 循環等待一定秒數直到看不見該店名為止，此時應該就更新完成
    time.sleep(wait)
    tbody_elements = driver.find_elements_by_xpath('//*[@id="inpage"]/div/div/div[2]/div/table/tbody/tr')
    return tbody_elements

def rowElementToSet(row:webdriver.remote.webelement) -> set:
    return {'店名':row.find_element_by_xpath('./td[2]').text,
            '地址':'中華民國 ' + row.find_element_by_xpath('./td[3]').text,
            '電話號碼':row.find_element_by_xpath('./td[4]').text,
            '藝文類型':row.find_element_by_xpath('./td[5]').text}

def getPageSize(driver:webdriver) -> int:
    "取得搜尋結果後，在table的tfoot元素內部取得有幾頁內容"
    # 從tfoot元素移動到內部的class = pagination元素，這個list保存所有分頁連結
    pagination = driver.find_element_by_css_selector('#inpage > div > div > div.rim > div > table > tfoot > tr > td > nav > ul')
    # 搜尋page-item的list
    pageitems = pagination.find_elements_by_class_name('page-item')
    # 搜尋到的list會多出4個(最前頁,上一頁,下一頁,最後頁)
    return len(pageitems) - 4

def searchByKey(query:str) -> pd.DataFrame:
    # 建立一個空的DataFrame
    result = pd.DataFrame({ "店名": [],"地址": [],"電話號碼": [],"藝文類型":[] })
    
    # 沒有輸入 => 空值
    if not query.strip():
        print("[Error]輸入空字串!")
        return result
    
    driver = webdriver.Chrome('chromedriver.exe') # 開啟webdriver
    driver.get('https://artsfungo.moc.gov.tw/promote_s/public/store') # 開啟藝fun卷:合作業者
    setQueryString(driver,query) # 設定搜尋關鍵字
    clickSearchBtn(driver) # 按下搜尋紐後會發生兩件事:顯示搜尋結果，跳出頁數選擇
    rows:list = waitForSearchResult(driver,7) # 等待搜尋內容跳出，如果有結果則收集結果(第一頁)
    
    # rows為空表示查無資料
    if not rows:
        print('[Info]查無資料')
        driver.close()
        return result
    
    # 將rows(第一頁)內容記錄在list
    for row in rows:
        result = result.append(rowElementToSet(row),ignore_index=True)
    
    # get Table page size form <tfoot>
    pageSize = getPageSize(driver)
    # 如果有第二頁(以上)，繼續抓取
    for i in range(2,pageSize+1):
        print(f'Scraping page {i}...')
        # 按"下一頁"
        driver.find_element_by_link_text("下一頁").click()
        # 等待下一頁table加載
        rows:list = waitForSearchUpdate(driver,2)
        for row in rows:
            result = result.append(rowElementToSet(row),ignore_index=True)

    # 收集結束
    driver.close()
    return result

query:str = input("請輸入查詢關鍵字:")
# data:pd.DataFrame = searchByKey('嘉義市') # about 25.4 sec
data:pd.DataFrame = searchByKey(query)
# 保存檔案
data.to_csv('data.csv')
