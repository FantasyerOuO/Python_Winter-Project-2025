# BeautifulSoup 示範
from bs4 import BeautifulSoup
import requests, pandas as pd
from pprint import pprint  # 美化輸出

# =======================
# 📌 Step 1: 請求網頁
# =======================
url = "https://www.twking.cc/"  # 目標網站
requests_01 = requests.get(url)  # 發送 HTTP GET 請求
requests_01.encoding = "utf8"  # 設定編碼，避免亂碼

# =======================
# 📌 Step 2: 解析網頁內容
# =======================
soup = BeautifulSoup(requests_01.text, "html.parser") 

# 找出所有 class 為 "booktop" 的 <div> 區塊（這是排行榜區塊）
booktops = soup.find_all("div", attrs={"class": "booktop"})

# =======================
# 📌 Step 3: 初步查看數據結構
# =======================
# 遍歷所有排行榜區塊，看看裡面的 HTML 結構
for top in booktops:
    for book in top:
        print(book.text.strip())  # 印出書名
    print("-" * 20)  # 分隔線

# =======================
# 📌 找出排行 Sol1 (使用 find_all)
# =======================
for booktop in booktops:
    tops = booktop.find_all('p')  # 找出這個區塊內的所有 <p> 標籤

    # 確保有數據再繼續執行，避免 IndexError
    if tops:
        top_type = tops[0].text.strip()  # 取得排行榜類型（例如「本週熱門」）
        print(top_type)

        for top in tops:
            if top.a:  # 確保 <p> 內有 <a>，避免 `NoneType` 錯誤
                print('\t', top.a.text.strip(), ':', top.a.get("href"))

    print("=" * 25)  # 分隔線

# =======================
# 📌 找出排行 Sol2 (使用 CSS Selector)
# =======================
for booktop in booktops:
    top_type = booktop.find("p").text.strip()  # 確保是 `<p>` 而不是 `P`
    tops = booktop.select("p a")  # 用 CSS 選擇器選取所有 <p> 內的 <a>

    print(top_type)

    for top in tops:
        print('\t', top.text.strip(), ':', top.get('href'))

    print("=" * 25)  # 分隔線

# =======================
# 📌 Step 4: 蒐集所有書籍資訊（去重、統計）
# =======================
booktop_summarize = {}  # 儲存結果的字典

for booktop in booktops:
    books = booktop.find_all('p')  # 找出這個排行榜區塊內所有 <p>

    for book in books[1:]:  # 跳過第一個 <p>（通常是排行榜類型）
        if book.a:  # 確保 <p> 內有 <a>，避免 `NoneType` 錯誤
            book_name = book.a.text.strip()  # 書名
            book_url = book.a.get("href")  # 書的超連結

            if book_name in booktop_summarize:
                booktop_summarize[book_name]["count"] += 1  # 已存在於紀錄，計數 +1
            else:
                booktop_summarize[book_name] = {
                    "count": 1,  # 初始計數 1
                    "href": book_url  # 儲存書的連結
                }

# =======================
# 📌 Step 5: 美化輸出結果
# =======================
# pprint(sorted(booktop_summarize.items(), 
#               reverse=True, 
#               key=lambda x:x[1]["count"]))

sorted_booktop_summarize = sorted(booktop_summarize.items(), reverse=True, key=lambda x:x[1]["count"]) # reverse:降幕排序

# 編譯表單呈現格式
book_rows=[]
for book in sorted_booktop_summarize:
    book_name = book[0]
    book_count = book[1]["count"]
    book_url = book[1]["href"]
    book_row = {
        "book name":book_name,
        "book count":book_count,
        "book url":book_url
                }
    book_rows.append(book_row)
booktop_summarize_df = pd.DataFrame(book_rows)
booktop_summarize_df.to_csv("booktop.csv")