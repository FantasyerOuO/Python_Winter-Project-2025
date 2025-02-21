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