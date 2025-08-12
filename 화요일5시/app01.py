from flask import Flask, render_template

app = Flask(__name__)

# http://127.0.0.1:5000/
@app.route("/")
def home():
    return render_template("index.html")

# http://127.0.0.1:5000/about
@app.route("/about")
def about():
    return "자기소개 페이지 입니다"

# http://127.0.0.1:5000/user/???
@app.route("/user/<username>")
def show_user_profile(username):
    return f"사용자 : {username}"
    
# templates 


if __name__ == "__main__":
    app.run(debug=True)
