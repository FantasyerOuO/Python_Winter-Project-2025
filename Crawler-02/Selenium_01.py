from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

# Step 1: 啟動瀏覽器 WebDriver（這裡使用 Microsoft Edge）
driver = webdriver.Edge()

# Step 2: 前往 Selenium 官方測試頁面
driver.get("http://selenium.dev/selenium/web/web-form.html")

# Step 3: 獲取當前頁面的標題（可用於驗證是否成功開啟網頁）
title = driver.title

# Step 4: 設定隱式等待 0.5 秒
# Selenium 會在查找元素時最多等待 0.5 秒，期間如果找到則立即執行
driver.implicitly_wait(1)

# Step 5.1: 使用 Selenium 抓取網頁元素，與 BeautifulSoup 的對照
# text_box  = soup.find(name="my-text")  # BeautifulSoup 查找 name 屬性為 "my-text" 的元素
text_box = driver.find_element(by=By.NAME, value="my-text")  # Selenium 查找 name 屬性為 "my-text" 的輸入框

# textarea_box  = soup.find("textarea")  # BeautifulSoup 查找 <textarea> 標籤
textarea_box = driver.find_element(by=By.TAG_NAME, value="textarea")  # Selenium 查找 textarea 標籤

# submit_button  = soup.select("button")  # BeautifulSoup 使用 CSS 選擇器查找 <button>
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")  # Selenium 使用 CSS 選擇器查找按鈕

# password_box = soup.find(name="my-password")  # BeautifulSoup 查找 name 屬性為 "my-password" 的輸入框
password_box = driver.find_element(by=By.NAME, value="my-password")  # Selenium 查找 name 屬性為 "my-password" 的輸入框

time.sleep(5)  # 等待 5 秒，確保頁面元素載入完全（非最佳做法，可改為顯式等待）

# Step.5.2 : 使用下拉選單，找到並使用
DropDown = driver.find_element(By.XPATH, "//select[@class='form-select' and @name='my-select']")
number_select = Select(DropDown)
number_select.select_by_visible_text(text="Two")

# Step 6: 填寫表單數據並提交
text_box.send_keys("Selenium")  # 輸入文字 "Selenium"
textarea_box.send_keys("OOOOXXXX")  # 輸入多行文本
password_box.send_keys("VVVVVVOOOO")  # 輸入密碼
time.sleep(5)
submit_button.click()  # 點擊提交按鈕

# Step.7
message = driver.find_element(by=By.CLASS_NAME, value="container")
print(message.text)
time.sleep(5)  # 等待 5 秒，確保表單送出後的效果可見

driver.quit()  # 關閉瀏覽器
