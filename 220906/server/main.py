from flask import Flask

app = Flask(__name__)       # __name__: 파일의 이름

@app.route('/')     # 127.0.0.1:5000/ 로 접속했을 때 바로 밑에 함수를 실행

def index() :
    return 'Hello World!'

@app.route('/second')       # 127.0.0.1:5000/second 웹브라우저를 이용하여 요청했을 때 바로 밑에 함수를 실행

def second() :
    return 'Second page'

app.run()


# 경로 들어가서 python3 main.py 실행