import pandas as pd, requests
from bs4 import BeautifulSoup

# ====================
# Step.1 讀取主頁排行榜資訊
# =====================

booktop_file = pd.read_csv(r"booktop.csv")

#先取前10筆資訊
booktop_10 = booktop_file
# print(booktop_10)
# 試提取資訊內容
last_chapter_titles, last_chapter_urls, last_chapter_counts = list(), list(), list()
for booktop in booktop_10.iterrows():
    # print(booktop[1]["book name"], booktop[1]["book url"])
# ====================
# Step.2 爬蟲小說頁面
# =====================
    page_url = booktop[1]["book url"]  # 目標網站
    requests_01 = requests.get(page_url)  # 發送 HTTP GET 請求
    requests_01.encoding = "utf8"  # 設定編碼，避免亂碼
    page_soup = BeautifulSoup(requests_01.text, "html.parser") # 解析網頁

    # 找出所有 class 為 "info-chapter" 的 <div> 區塊（這是排行榜區塊）
    # div.info-chapters.flex.flex-wrap
    book_page = page_soup.find("div", attrs={"class": "info-chapters"})
    
    chapters = book_page.find_all("a")
    
    last_chapter_counts.append(len(chapters))
    last_chapter_titles.append(chapters[-1].get("title"))
    last_chapter_urls.append(chapters[-1].get("href"))

booktop_file.loc[:, "chapters"] = last_chapter_counts
booktop_file.loc[:, "Last chapter title"] = last_chapter_titles
booktop_file.loc[:, "Last chapter url"] = last_chapter_urls

booktop_file.to_csv("booktop_last.csv")