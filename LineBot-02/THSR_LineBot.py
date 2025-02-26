from flask import Flask, request, abort
from THSR_Booker_ChatDeal_GPT import ChatGPT
from THSR_Booker_main import *
from datetime import datetime

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

import os, json

# 設定系統
app = Flask(__name__)
configuration = Configuration(access_token=os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# 取得當前時間
current_datetime = datetime.now()
current_date = current_datetime.strftime("%Y-%m-%d")  # 2025-02-21
current_time = current_datetime.strftime("%H:%M")  # 14:30
current_chinese_date = current_datetime.strftime("%m月%d日%Y年")  # 03月10日2025年

# 使用者資料和狀態紀錄
user_Data = {}

# 設定標準車票訂購資訊
data_format = {
    "出發站":"出發站",
    "抵達站":"抵達站",
    "出發日期":"中文月份 %d, %Y",
    "出發時間":"%H:%M"
}

# 取得使用者資料和狀態
def Get_user_Data(user_ID):
    return user_Data.get(user_ID, {})
# 更新使用者資料和狀態
def Update_user_Data(user_ID, **Info_Dict):
    if user_ID not in user_Data:
        user_Data[user_ID] = Info_Dict
    else:
        Info_has_value = {
            slot_Name : slot_Value
            for slot_Name,slot_Value in  Info_Dict.items() if slot_Value
        }
        user_Data[user_ID].update(Info_has_value)

# 檢查webhook是否正常運作
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'




# BOT 服務中...
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    BOT_Response = "發生錯誤，請稍後再試..。"
    print(user_Data)
    # 取得使用者資料和訊息
    user_ID = event.source.user_id
    user_Msg = event.message.text
    # 設定THSR訂票資訊(需獲取 出發站、抵達站、出發日期、出發時間)
    Required_Book_Info = ["出發站", "抵達站", "出發日期", "出發時間"]
    # 確認使用者狀態
    if user_Data.get("Intent", "") != "高鐵訂票" and user_Msg == "高鐵訂票":     # 假設使用者狀態不是高鐵訂票，且使用者輸入高鐵訂票，則更新使用者狀態 # Intent: 意圖(狀態)
        Update_user_Data(user_ID, Intent="高鐵訂票")                
        BOT_Response = "請輸入你的高鐵訂位資訊，需包含：出發站、抵達站、出發日期、出發時間。" # BOT 回應
    # 如果使用者狀態為高鐵訂票
    elif user_Data.get("Intent") == "高鐵訂票": 
        unfilled_Slots = [key for key in Required_Book_Info if not user_Data.get(key)] # 塞選未被填寫的欄位
    
        # 開始填寫訂票資訊
        # 設定ChatGPT提示詞
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
    - 時間格式須為 **「小時:分鐘」**（例如：*{{current_time}}*）。
    - 二月只有28天，請注意日期的合理性。
    - **出發站和抵達站請使用中文名稱。**
    - **請記住當前時間為{{current_datetime}}。**
    - **若其他資訊缺失，請用空字串 `""` 填補。**
    - **只回傳python dictionary格式，請勿輸出其他文字或對話！**
    - **出發站和抵達站不能相同，如果相同則抵達站用空字串`""`填補！**
                    """
        # ChatGPT處理輸入訊息
        ChatGPT_Msg_Deal = ChatGPT(System_Prompt=sys_prompts, User_Message=user_Msg)
        Data_Convert_Dict = json.loads(ChatGPT_Msg_Deal.replace("'", "\""))
        Update_user_Data(user_ID, **Data_Convert_Dict)

         # 判斷已填的資訊
        user_data = Get_user_Data(user_ID)  # 重新讀取一次user_data
        filled_slots = [
            # 已填的資訊
            key for key in Required_Book_Info if user_data.get(key)]
        unfilled_slots = [
            # 未填的資訊
            key for key in Required_Book_Info if not user_data.get(key)]

        app.logger.info(f"filled_slots: {filled_slots}")
        app.logger.info(f"unfilled_slots: {unfilled_slots}")
        app.logger.info(f"機器人回應: {BOT_Response}")

        # if unfilled_Slots:
        #     ChatGPT_Msg_Deal = ChatGPT(System_Prompt=sys_prompts, User_Message=user_Msg) # 處理使用者訊息
        # # 轉換ChatGPT回傳的資料為字典(ChatGPT回傳的資料為字串)
        #     Data_Convert_Dict = json.loads(ChatGPT_Msg_Deal.replace("'", "\"")) # 轉換字串為字典
        # # 更新使用者資料
        #     Update_user_Data(user_ID, Data_Convert_Dict)
        # # 確認是否有未填寫的欄位
        #     unfilled_Slots = [key for key in Required_Book_Info if not user_Data.get(key)]
        # # 如果有未填寫的欄位，則BOT回應
        if len(unfilled_Slots) != 0:
            BOT_Response = f"請提供: {', '.join(unfilled_Slots)}"
        else:
            THSR_create_driver()
            THSR_Cookie()
            THSR_user_set(
                user_Data[user_ID]["出發站"], 
                user_Data[user_ID]["抵達站"], 
                user_Data[user_ID]["出發日期"], 
                user_Data[user_ID]["出發時間"])
            # 取得車次資訊
            Trains_Info = THSR_trains_Info()
            Trains_Info_Message = ""  # 車次資訊字串
            for idx, train in enumerate(Trains_Info):
                Trains_Info_Message += (f"({idx}) - {train['train_code']}, 行駛時間={train['duration']} | {train['depart_time']} -> {train['arrival_time']}\n")
            BOT_Response = f"以下是目前可選擇的車次，請選擇欲搭乘的車次\n {Trains_Info_Message}"
            # 更新使用者狀態
            Update_user_Data(user_ID, Intent = "車次選擇", Trains_Info = Trains_Info)

    # 如果使用者狀態為車次選擇
    elif user_Data.get("Intent") == "車次選擇":
        system_prompt = f"""
            1.瞭解目前使用者的可以做的選擇有哪些，選擇項目請查看{THSR_trains_Info()}
            2.將車次資訊依順序從0排到n(車次資訊的長度)
            3.分析使用者的言詞判斷是指順序數字、出發時間、抵達時間、行駛時間還是車次代碼
            4.將使用者的選擇轉換成對應的車次資訊
            5.將車次資訊轉換成對應的對應到順序
            **6.只提取順序數字，不回傳其他文字**
        """
        user_Train_Select = int(ChatGPT(System_Prompt=system_prompt, User_Message=user_Msg))
        THSR_Train_Select(user_Train_Select)
        
        user_Data["Intent"] = "輸入個資"
    
    # 如果使用者狀態為輸入個資
    elif user_Data.get("Intent") == "輸入個資":
        # BOT訊息
        BOT_Response = "請輸入你的高鐵訂位資訊，需包含：身分證號碼、電話號碼、E-Mail。"  # BOT 回應

        # 針對 Person_Info 進行設定
        user_Person_Info = {
            "身分證": "", 
            "手機號碼": "", 
            "E-Mail": ""
        }

        def Update_user_Person_Info(data_dict):
            """更新使用者的個人資訊"""
            for key, value in data_dict.items():
                if key in user_Person_Info:  # 確保 key 存在於字典
                    user_Person_Info[key] = value  # 直接更新值

        Required_Person_Info = ["身分證", "手機號碼", "E-Mail"]
        unfilled_Slots = [key for key in Required_Person_Info if not user_Person_Info.get(key)]  # 塞選未填寫的欄位

        # 設定 ChatGPT 提示詞
        sys_prompts = f"""
            提取對話中符合 `{{user_Person_Info}}` 的資料，包含：
            - **身分證**
            - **手機號碼**
            - **E-Mail**
            並且將其**替換** `{{user_Person_Info}}` 中的對應值。

            ### **請遵循以下規則：**
            - **身分證格式為首字英文字母加上9碼數字，例如 A123456789**
            - **手機號碼格式為 10 碼數字，且以 `09` 開頭，例如：0912345678** 
            - **E-Mail 格式必須包含 @，符合標準 Email 格式，域名須由字母、數字及 . 組成，結尾需為有效頂級域名（.com、.tw 等）**
            - 範例：test123@example.com、user.name@domain.tw
            - **若其他資訊缺失或錯誤，請用空字串 `""` 填補。**
            - **將對應資料提取後對應 `{{user_Person_Info}}` 寫入，只回傳 Python dictionary 格式，請勿輸出其他文字或對話！**
        """

        # ChatGPT 處理輸入訊息
        if unfilled_Slots:
            ChatGPT_Msg_Deal = ChatGPT(System_Prompt=sys_prompts, User_Message=user_Msg)  # 處理使用者訊息
            # 轉換 ChatGPT 回傳的資料為字典（ChatGPT 回傳的資料為字串）
            Data_Convert_Dict = json.loads(ChatGPT_Msg_Deal.replace("'", "\""))  # 轉換字串為字典
            # 更新使用者資料
            Update_user_Person_Info(Data_Convert_Dict)

            # 確認是否有未填寫的欄位
            unfilled_Slots = [key for key in Required_Person_Info if not user_Person_Info.get(key)]

        # 如果有未填寫的欄位，則 BOT 回應
        if len(unfilled_Slots) != 0:
            BOT_Response = f"請提供: {', '.join(unfilled_Slots)}"

        else:
            THSR_Person_Info_input(
                user_Person_Info["身分證"],
                user_Person_Info["手機號碼"],
                user_Person_Info["E-Mail"]
            )
            THSR_Privacy_Policy_Check()
            BOT_Response = "訂票成功！"
            user_Data["Intent"] = "訂票成功"
    

    # 回覆使用者訊息
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        # if BOT_Response.strip() in ["請稍後...1", "請稍後...2"]:
            
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                # 回覆使用者的訊息
                messages=[
                    # 這邊是回覆給使用者的訊息內容
                    TextMessage(text=BOT_Response) 
                    ]
            )
        )
    
     

if __name__ == "__main__":
    app.run(debug=True)
    

    
# @handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         line_bot_api.reply_message_with_http_info(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 # 回覆使用者的訊息
#                 messages=[
#                     # 這邊是回覆給使用者的訊息內容
#                     TextMessage(text=event.message.text) 
#                     ]
#             )
#         )
