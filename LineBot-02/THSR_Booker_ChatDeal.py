from THSR_Booker_ChatDeal_GPT import ChatGPT
import THSR_Booker_main
import json
from datetime import datetime

data_format = {
    "出發站":"出發站",
    "抵達站":"抵達站",
    "出發日期":"中文月份-%d-%Y",
    "出發時間":"%H:%M"
}

# 取得當前時間
current_datetime = datetime.now()
current_date = current_datetime.strftime("%Y-%m-%d")  # 2025-02-21
current_time = current_datetime.strftime("%H:%M")  # 14:30
current_chinese_date = current_datetime.strftime("%m月%d日%Y年")  # 03月10日2025年

# 重新編譯 GPT 提示詞，加入 `*` 符號來強調關鍵內容
sys_prompts = f"""
請**只**提取對話中的**高鐵訂位資訊**，符合 `{{data_format}}` 的格式，包含：
- **出發站**
- **抵達站**
- **出發日期**
- **出發時間**
並且將其**替換** `{{data_format}}` 中的對應值。

臺灣高鐵所有站名及其所在地區: (臺北)南港、(臺北)台北、(新北)板橋、(桃園)桃園、(新竹)新竹、(苗栗)苗栗、(臺中)台中、(彰化)彰化、(雲林)雲林、(嘉義)嘉義、(臺南)台南、(高雄)左營。
- **如果指的是地區將其轉換成對應車站名稱，如:使用者:高雄, 輸出:左營。**


### **請遵循以下規則：**
- 日期格式須為 **「中文數字月份「/」日期「/」年份」**（例如：*十月/10/2025*）。
- 時間格式須為 **「小時:分鐘」**（例如：*{current_time}*）。
- 二月只有28天，請注意日期的合理性。
- **出發站和抵達站請使用中文名稱。**
- **請記住當前時間為{current_datetime}。**
- **若其他資訊缺失，請用空字串 `""` 填補。**
- **只回傳字典，請勿輸出其他文字或對話！**
- **出發站和抵達站不能相同，如果相同則抵達站用空字串`""`填補！**
"""

# 輸入訂票資訊
def request_Book_Info():
    # print("Ask booking information")
    user_response = input("請輸入你的高鐵訂位資訊，請提供:出發站、抵達站、出發日期、出發時間\n")
    user_response_info = ChatGPT(System_Prompt=sys_prompts, User_Message=user_response)
    print(type(user_response_info))
    user_book_info = json.loads(user_response_info.replace("'", "\""))
    return user_book_info

# 複檢訂票資訊有無錯誤
def request_Miss_Book_Info(user_Book_Info):
    # print("Ask miss booking information")   
    while any(value == "" for value in user_Book_Info.values()):
        missing_keys = [key for key, value in user_Book_Info.items() if value == ""]
        if missing_keys:
            user_response = input("有遺漏的資訊喔，請提供：{}\n".format(", ".join(missing_keys)))  
            user_response_info = ChatGPT(System_Prompt=sys_prompts, User_Message=user_response)             
        try:
            user_response_info = json.loads(user_response_info.replace("'", "\""))
            user_Book_Info = {key:user_Book_Info[key] if user_Book_Info[key] != "" else user_response_info[key] for key in user_Book_Info}
        except:
            continue
    else:
        return user_Book_Info

ID_data_format = {
    "身分證":"A123456789",
    "手機號碼":"0912345678",
    "E-Mail":"Test@gmail.com"
}

sys_prompts_2 = f"""
提取對話中符合 `{{ID_data_format}}` 的資料，包含：
- **身分證**
- **手機號碼**
- **E-Mail**
並且將其**替換** `{{ID_data_format}}` 中的對應值。

### **請遵循以下規則：**
- **身分證格式為首字英文字母加上9碼數字,例如A123456789**
- **手機號碼格式為10碼數字而且以`09`開頭,例如:0912345678** 
- **E-Mail格式為必須包含 @，符合標準 Email 格式，域名須由字母、數字及 . 
組成，結尾需為有效頂級域名（.com、.tw 等）,
範例：test123@example.com、user.name@domain.tw**
- **若其他資訊缺失或錯誤，請用空字串 `""` 填補。**
- **將對應資料提取後對應{ID_data_format}寫入，只回傳字典，請勿輸出其他文字或對話！**
"""

def request_Person_Info():
    # print("Ask booking information")
    user_response = input("請輸入你的身分證、手機號碼、E-Mail:\n")
 
    user_response_info = ChatGPT(System_Prompt=sys_prompts_2, User_Message=user_response)
    # print(type(user_response_info))
    user_Person_info = json.loads(user_response_info.replace("'", "\""))
    return user_Person_info

def request_Miss_Peraon_Info(user_Person_Info):
    # print("Ask miss person information")   
    while any(value == "" for value in user_Person_Info.values()):
        missing_keys = [key for key, value in user_Person_Info.items() if value == ""]
        if missing_keys:
            user_response = input("有遺漏的資訊喔，請提供：{}\n".format(", ".join(missing_keys)))  
            user_response_info = ChatGPT(System_Prompt=sys_prompts_2, User_Message=user_response)             
        try:
            user_response_info = json.loads(user_response_info.replace("'", "\""))
            user_Person_Info = {key:user_Person_Info[key] if user_Person_Info[key] != "" else user_response_info[key] for key in user_Book_Info}
        except:
            continue
    else:
        print(user_Person_Info)
        return user_Person_Info


if __name__ == "__main__":

    user_Book_Info = request_Book_Info()
    # print(type(user_Book_Info))
    user_Book_Info = request_Miss_Book_Info(user_Book_Info)
    # print(user_Book_Info["出發時間"])

    

    