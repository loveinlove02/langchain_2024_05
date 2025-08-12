from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 로그인 페이지 (GET/POST 요청 모두 처리)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 사용자가 입력한 아이디와 비밀번호를 가져옵니다.
        username = request.form['username']
        password = request.form['password']

        # 아이디가 'admin'이고 비밀번호가 '1234'이면 로그인 성공
        if username == 'admin' and password == '1234':
            # 로그인 성공 시 main 페이지로 리다이렉트합니다.
            return redirect(url_for('main', username=username))
        else:
            # 로그인 실패 시 에러 메시지와 함께 다시 로그인 페이지를 보여줍니다.
            error = '아이디 또는 비밀번호가 올바르지 않습니다.'
            return render_template('index.html', error=error)
    
    # GET 요청일 경우, 로그인 페이지를 렌더링합니다.
    return render_template('index.html')

# 메인 페이지
@app.route('/main/<username>')
def main(username):
    # 로그인 성공 시 전달받은 username을 main.html에 넘겨줍니다.
    return render_template('main.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
