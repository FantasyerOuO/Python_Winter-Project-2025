import time, pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from ocr_component_Teacher import get_captcha_code
from Radom_ID import random_ID_Gerenate, random_Phone_Number_Gerenate, random_Email_Gerenate

# 設定 WebDriver 選項
# 設定 Chrome 瀏覽器的選項，禁用自動化控制特徵，以防止網站偵測到 Selenium 機器人
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

# 進入台灣高鐵訂票網站
# 使用 driver.get() 方法打開高鐵官方網站

driver.get("https://irs.thsrc.com.tw/IMINT/")

# 第一個頁面 - 接受 Cookie
# 找到並點擊接受 Cookie 按鈕，確保頁面能夠正常運作
driver.find_element(By.ID, "cookieAccpetBtn").click()

# 第一個頁面 - 選擇出發站和目的地
# 透過 Select 類別選擇出發與目的地車站
Select(driver.find_element(By.NAME, 'selectStartStation')).select_by_visible_text('台中')
Select(driver.find_element(By.NAME, 'selectDestinationStation')).select_by_visible_text('板橋')

# 第一個頁面 - 選擇時間
# 選擇出發時間，確保符合需求
Select(driver.find_element(By.NAME, 'toTimeTable')).select_by_visible_text('18:30')

# 第一個頁面 - 選擇日期
# 點擊日期選擇框，然後選擇特定日期（2025 年 2 月 21 日）
driver.find_element(By.XPATH, "//input[@class='uk-input' and @readonly='readonly']").click()
driver.find_element(By.XPATH, "//span[@class='flatpickr-day' and @aria-label='二月 27, 2025']").click()

# 第一個頁面 - 驗證碼處理
# 進行驗證碼的自動輸入，透過 OCR 辨識圖片中的驗證碼
while True:
    driver.find_element(By.ID, 'BookingS1Form_homeCaptcha_passCode').screenshot('captcha.png')
    captcha_code = get_captcha_code()
    driver.find_element(By.ID, 'securityCode').send_keys(captcha_code)
    time.sleep(2)
    driver.find_element(By.ID, 'SubmitButton').click()
    
    # 第一個頁面 - 驗證是否成功
    # 嘗試檢查是否成功進入下一步，若未進入則重新輸入驗證碼
    try:
        time.sleep(5)
        driver.find_element(By.ID, 'BookingS2Form_TrainQueryDataViewPanel')
        print("驗證碼正確, 進到第二步驟")
        break
    except NoSuchElementException:
        print("驗證碼錯誤，重新驗證")

# 第二個頁面 - 取得車次資訊
# 取得所有可選擇的車次資訊，並儲存為列表
trains_info = []
trains = driver.find_element(By.CLASS_NAME, 'result-listing').find_elements(By.TAG_NAME, 'label')

for train in trains:
    info = train.find_element(By.CLASS_NAME, 'uk-radio')
    trains_info.append({
        'depart_time': info.get_attribute('querydeparture'),
        'arrival_time': info.get_attribute('queryarrival'),
        'duration': info.get_attribute('queryestimatedtime'),
        'train_code': info.get_attribute('querycode'),
        'radio_box': info,
    })

# 第二個頁面 - 列印車次資訊
# 使用 pprint 以更易讀的格式列出所有車次資訊
pprint.pprint(trains_info)

# 第二個頁面 - 列出所有車次並讓使用者選擇
# 顯示所有可選車次，讓使用者輸入編號選擇
for idx, train in enumerate(trains_info):
    print(f"({idx}) - {train['train_code']}, 行駛時間={train['duration']} | {train['depart_time']} -> {train['arrival_time']}")

which_train = int(input("Choose your train. Enter from 0~9:\n"))
# which_train = 0
trains_info[which_train]['radio_box'].click()

# 第二個頁面 - 確認訂票
# 點擊提交按鈕以完成訂票程序
driver.find_element(By.NAME, 'SubmitButton').click()


# 第三個頁面 - 輸入訂票個資
ID_Input = driver.find_element(By.ID, "idNumber")
ID_Input.send_keys(random_ID_Gerenate())
PhoneNumber_Input = driver.find_element(By.ID, "mobilePhone").send_keys(random_Phone_Number_Gerenate())
Email_Input = driver.find_element(By.ID, "email").send_keys(random_Email_Gerenate())

# 第三個頁面 - 點選同意個資法使用
check_box = driver.find_element(By.XPATH, "//input[@name='agree' and @class='uk-checkbox']").click()
finally_submit_btn = driver.find_element(By.XPATH, "//input[@id='isSubmit' and @type='button']").click()

# 暫停一段時間觀察結果
# 延遲 2000 秒確保頁面能夠完整載入後才關閉
# 這段時間內使用者可以手動確認訂票狀態
time.sleep(20)
driver.quit()
