import time, pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from THSR_Booker_OCR import get_captcha_code
from THSR_Booker_ChatDeal_GPT import ChatGPT

def THSR_create_driver():
    # 設定 WebDriver 選項
    # 設定 Chrome 瀏覽器的選項，禁用自動化控制特徵，以防止網站偵測到 Selenium 機器人
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    global driver
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

# 進入台灣高鐵訂票網站
# 使用 driver.get() 方法打開高鐵官方網站
def THSR_Cookie():
    driver.get("https://irs.thsrc.com.tw/IMINT/")
    driver.find_element(By.ID, "cookieAccpetBtn").click()   
    driver.implicitly_wait(5)

# 第一個頁面 - 選擇訂票資訊
# 選擇出發站、抵達站、出發日期、出發時間，並輸入驗證碼
def THSR_user_set(start_station, destination_station, Departure_Date, Departure_Time):
    # 站點選擇
    Select(driver.find_element(By.NAME, 'selectStartStation')).select_by_visible_text(start_station)
    Select(driver.find_element(By.NAME, 'selectDestinationStation')).select_by_visible_text(destination_station)
    # 出發日期
    Departure_Date = Departure_Date.split("/")  
    Departure_Date_str = f"{Departure_Date[0]} {Departure_Date[1]}, {Departure_Date[2]}"                   
    driver.find_element(By.XPATH, "//input[@class='uk-input' and @readonly='readonly']").click()
    driver.find_element(By.XPATH, f"//span[@class='flatpickr-day' and @aria-label='{Departure_Date_str}']").click()
    # 出發時間
    Select(driver.find_element(By.NAME, 'toTimeTable')).select_by_visible_text(Departure_Time)
    # 驗證碼
    while True:
        driver.find_element(By.ID, 'BookingS1Form_homeCaptcha_passCode').screenshot('captcha.png')
        captcha_code = get_captcha_code()
        driver.find_element(By.ID, 'securityCode').send_keys(captcha_code)
        time.sleep(2)
        driver.find_element(By.ID, 'SubmitButton').click()
        try:
            time.sleep(5)
            driver.find_element(By.ID, 'BookingS2Form_TrainQueryDataViewPanel')
            print("驗證碼正確, 進到第二步驟")
            break
        except NoSuchElementException:
            print("驗證碼錯誤，重新驗證")
    driver.implicitly_wait(5)

# 第二個頁面 - 取得車次資訊
# 取得所有可選擇的車次資訊，並儲存為列表
# 第二個頁面 - 列出所有車次並讓使用者選擇
# 顯示所有可選車次，讓使用者輸入編號選擇
def THSR_train_Info():
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
    # return trains_info
# def Train_Select(trains_info):
    for idx, train in enumerate(trains_info):
            pprint.pprint(f"({idx}) - {train['train_code']}, 行駛時間={train['duration']} | {train['depart_time']} -> {train['arrival_time']}")
    user_response = input("你想搭乘哪一班次呢?:\n")
    system_prompt = f"""
                1.瞭解目前使用者的可以做的選擇有哪些，選擇項目請查看{trains_info}
                2.將車次資訊依順序從0排到n(車次資訊的長度)
                3.分析使用者的言詞判斷是指排列順序、出發時間、抵達時間、行駛時間還是車次代碼
                4.將使用者的選擇轉換成對應的車次資訊
                5.將車次資訊轉換成對應的對應到順序
                **6.只提取順序數字，不回傳其他文字**
            """
    which_train = int(ChatGPT(System_Prompt=system_prompt, User_Message=user_response))
    print(which_train)
    trains_info[which_train]['radio_box'].click()
    driver.find_element(By.NAME, 'SubmitButton').click()
    driver.implicitly_wait(5)


# # 第三個頁面 - 輸入訂票個資
def THSR_Person_Info_input(ID, Phone_Number, Email):

    ID_Input = driver.find_element(By.ID, "idNumber").send_keys(ID)
    PhoneNumber_Input = driver.find_element(By.ID, "mobilePhone").send_keys(Phone_Number)
    Email_Input = driver.find_element(By.ID, "email").send_keys(Email)
    driver.implicitly_wait(5)

# 第三個頁面 - 點選同意個資法使用
def THSR_Privacy_Policy_Check():
    check_box = driver.find_element(By.XPATH, "//input[@name='agree' and @class='uk-checkbox']").click()
    # finally_submit_btn = driver.find_element(By.XPATH, "//input[@id='isSubmit' and @type='button']").click()
    driver.implicitly_wait(5)

def THSR_Webdriver_Quit():
    time.sleep(20000)
    driver.quit()
