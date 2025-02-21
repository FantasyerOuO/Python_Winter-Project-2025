# Flask 入門教學範本

## 介紹

這是一個使用 Flask 架設的 Web 應用程式範本，包含：

1. **首頁** - 顯示基本首頁模板。
2. **使用者資訊輸入頁面** - 允許使用者輸入名稱並提交。
3. **ChatGPT 對話系統** - 讓使用者與 ChatGPT 進行互動。
4. **測試動態路由** - 演示如何使用 Flask 處理 URL 參數。

本範例示範了如何使用 Flask 來處理表單請求 (`POST` 方法) 以及與 OpenAI 的 ChatGPT 互動。

---

## **1. 安裝 Flask 及 OpenAI API**

在開始之前，請確保你已安裝 Flask 及 OpenAI API：

```sh
pip install flask openai
```

---

## **2. 建立 Flask 應用程式 (`app.py`)**

```python
from flask import Flask, render_template, request
from werkzeug.utils import escape
from OpenAI_SDK_01_FlaskTest import ChatGPT  # 確保此模組存在

app = Flask(__name__)

# 1️⃣ **首頁 (Homepage)**
@app.route("/")
def hello_world():
    return render_template("homepage_html_sample.html")

# 2️⃣ **使用者名稱輸入測試**
@app.route("/nameInput_sample/")
def show_html_sample():
    return render_template("InfoInput_html_sample.html", name="範例:小明")

@app.route("/nameInput_sample/submit_name", methods=["POST"])
def submit_name():
    username = request.form.get("username", "")  # 取得表單的 username
    return render_template("nameInput_html_sample.html", name=username)

# 3️⃣ **ChatGPT 對話頁面**
@app.route("/ChatGPT_Test_Sample/")
def chat_page():
    return render_template("Flask_ChatGPT_Test_html_sample.html")

# 4️⃣ **ChatGPT API 端點**
@app.route("/ChatGPT_Test_py/<user_message>")
def ChatGPTTest(user_message):
    Promat_Word = "你是一個友善的 AI 助手，請根據使用者的問題提供簡單、清晰的回答。"
    chatpgt_response = ChatGPT(
        System_Prompt=Promat_Word,
        User_Message=user_message,
    )
    return chatpgt_response

# 5️⃣ **測試動態 URL 參數**
@app.route("/test/<path:subpath>")
def show_subpath(subpath):
    return f"<p>Hello PATH-{escape(subpath)}, World!</p>"

# 啟動 Flask 應用程式
if __name__ == "__main__":
    app.run(debug=True)
```

---

## **3. Flask HTML 範本結構**

你需要建立 `templates/` 資料夾，並在其中放置 HTML 檔案。

### **(1) `templates/homepage_html_sample.html` (首頁)**

```html
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>首頁</title>
</head>
<body>
    <h1>歡迎來到 Flask 教學範本</h1>
    <a href="/nameInput_sample/">前往名稱輸入頁面</a>
    <br>
    <a href="/ChatGPT_Test_Sample/">前往 ChatGPT 測試</a>
</body>
</html>
```

### **(2) `templates/InfoInput_html_sample.html` (名稱輸入頁面)**

```html
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>輸入你的名字</title>
</head>
<body>
    <h1>請輸入您的名字</h1>
    <form action="/nameInput_sample/submit_name" method="post">
        <input type="text" name="username" placeholder="請輸入您的名字" required>
        <button type="submit">送出</button>
    </form>
    {% if name %}
        <p>你的名字是：{{ name }}</p>
    {% endif %}
</body>
</html>
```

### **(3) `templates/Flask_ChatGPT_Test_html_sample.html` (ChatGPT 對話頁面)**

```html
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>ChatGPT 聊天</title>
</head>
<body>
    <h1>ChatGPT 測試</h1>
    <input type="text" id="userInput" placeholder="請輸入訊息">
    <button onclick="sendMessage()">送出</button>
    <p id="response">這裡會顯示回應</p>
    <script>
        function sendMessage() {
            let userMessage = document.getElementById("userInput").value;
            fetch(`/ChatGPT_Test_py/${encodeURIComponent(userMessage)}`)
                .then(response => response.text())
                .then(data => {
                    document.getElementById("response").innerText = data;
                });
        }
    </script>
</body>
</html>
```

---

## **4. 執行 Flask 應用程式**

確保你的 Flask 專案結構如下：

```
project_folder/
│── app.py  # Flask 主程式
│── templates/
│   ├── homepage_html_sample.html
│   ├── InfoInput_html_sample.html
│   ├── Flask_ChatGPT_Test_html_sample.html
```

### **啟動 Flask 伺服器**

你可以使用以下方式啟動 Flask：

#### **一般模式**
```sh
flask --app app run
```

#### **Debug 模式**
```sh
flask --app app run --debug
```

在瀏覽器中打開 `http://127.0.0.1:5000/`，開始測試！🎯

---

## **5. 總結**

這個範例示範了如何使用 Flask：

- **建立 Flask 伺服器**
- **處理使用者輸入** (`POST` 表單)
- **建立 ChatGPT 互動 API**
- **顯示動態回應**
- **動態 URL 參數處理**

這是 Flask Web 開發的基礎，學會後你可以擴展功能，例如：

- 增加更多互動功能
- 使用資料庫儲存輸入紀錄
- 建立更精美的前端設計

希望這份教學範本對你有幫助！🚀

