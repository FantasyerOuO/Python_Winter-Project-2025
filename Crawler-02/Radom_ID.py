import time, pprint, random, string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from ocr_component_Teacher import get_captcha_code

def random_ID_Gerenate():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)

    driver.get("https://people.debian.org/~paulliu/ROCid.html")

    driver.find_element(By.XPATH, "//input[@value='Generate']").click()
    randomID = driver.find_element(By.XPATH, "//input[@type='text' and @name='a' and @size='10']").get_attribute("value")
    
    driver.quit()
    
    return randomID
def random_Phone_Number_Gerenate():
    phone_number = "09" + "".join(str(random.randint(0, 9)) for _ in range(8))
    return phone_number

def random_Email_Gerenate():
    letters_part = ''.join(random.choices(string.ascii_letters, k=4))
    numbers_part = ''.join(random.choices(string.digits, k=6))
    return letters_part + numbers_part + "@gmail.com"


if __name__ == "__main__":
    random_ID_Gerenate()
    random_Phone_Number_Gerenate()
    random_Email_Gerenate()