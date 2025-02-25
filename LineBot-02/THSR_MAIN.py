from THSR_Booker_ChatDeal import *
from THSR_Booker_main import *

# step.1 輸入訂票資訊
user_Book_Info = request_Book_Info()
# step.2 複檢訂票資訊有無錯誤
user_Book_Info = request_Miss_Book_Info(user_Book_Info)
# step.3 進入台灣高鐵訂票網站
THSR_create_driver()
THSR_Cookie()
# step.4 選擇訂票資訊
THSR_user_set(user_Book_Info["出發站"], user_Book_Info["抵達站"], user_Book_Info["出發日期"], user_Book_Info["出發時間"])
# step.5 取得車次資訊
THSR_train_Info()
# step.6 輸入個人資訊並檢查
user_Person_Info = request_Person_Info()
user_Person_Info = request_Miss_Peraon_Info(user_Person_Info)
# step.7 輸入訂票個資
THSR_Person_Info_input(user_Person_Info["身分證"], user_Person_Info["手機號碼"], user_Person_Info["E-Mail"])
# step.8 點選同意個資法使用並送出
THSR_Privacy_Policy_Check()
# step.9 關閉瀏覽器
THSR_Webdriver_Quit()
