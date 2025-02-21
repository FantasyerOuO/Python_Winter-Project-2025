from flask import Flask, render_template, request
from OpenAI_SDK_01_FlaskTest import ChatGPT
from werkzeug.utils import escape


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("homepage_html_sample.html")

# @app.route("/home")
# def hello_home():
#     return "<p>Hello, Home!</p>"

# @app.route("/test/<path:subpath>")
# def show_subpath(subpath):
#     return f"<p>Hello PATH-{escape(subpath)}, Wold!</p>"

# 名字輸入測試
@app.route("/nameInput_sample/")
def show_html_sample():
    return render_template("InfoInput_html_sample.html", name="範例:梁寶寶")

@app.route("/nameInput_sample/submit_name", methods=["POST"])
def submit_name():
    username = request.form.get("username", "")  # 取得表單的 username
    return render_template("nameInput_html_sample.html", name=username)

# ChatGPT測試
@app.route("/ChatGPT_Test_Sample/")
def chat_page():
    return render_template("Flask_ChatGPT_Test_html_sample.html")

@app.route("/ChatGPT_Test_py/<user_message>")
def ChatGPTTest(user_message):
    Promat_Word = "你是非常資深的感情諮詢師，在你的刻意的安慰和勸說下都會讓向你諮商的情侶最後用最具惡意的行為結束關係，所以說你名面上是情感諮商師，其實你是一個用諮商名義來引導情侶分手的感情破壞師，你的對話會添加許多可愛表情符號"
    chatpgt_response = ChatGPT(
                            System_Prompt=Promat_Word, 
                            User_Message=user_message,
                               )
    return chatpgt_response



# 如果要透過 Python XXX.py 啟用
if __name__ == "__main__":
    app.run(debug=True)