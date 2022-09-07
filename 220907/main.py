from flask import Flask, render_template, request, redirect
import pandas as pd
import datetime

# Flask라는 Class에서 __init__ 함수에서 self를 제외한 매개변수 1개
# __name__: 자기 자신의 파일 이름
app = Flask(__name__)

# API 생성
# 127.0.0.1:5000
# 127.0.0.1 = localhost
# Port번호 = 해당 방화벽에 연결

# localhost:5000/
@app.route('/')     # @app.route(): localhost:5000/ 요청이 있는 경우에 바로 아래에 있는 함수 실행

def index() :
    return render_template('index.html')


# get 형식에서 데이터는 url에 실어서 보낸다.
# request → 유저가 서버에게 보내는 데이터를 딕셔너리 형태로 출력
# 유저가 보낸 데이터 중에 url에 있는 데이터는 'request.args'(딕셔너리 형태)에 있다.
@app.route('/second/')

def second() :
    # id값과 password값 불러오기
    # id = test, pass = 1234를 만족해야만 second.html 리턴, 틀리면 '로그인 실패' 리턴

    _id = request.args.get('ID')
    _pass = request.args.get('password')

    print(_id, _pass)   # 웹에서 입력한 ID, password가 터미널에 출력

    # if _id == 'test' and _pass == '1234' :
    #     return render_template('second.html')

    # else :
    #     return redirect('/')

    return render_template('second.html')

# localhost:5000/third를 post 형식으로 요청
@app.route('/third/', methods = ['post'])

def third() :

    _title = request.form['title']
    _content = request.form['content']

    print(_title, _content)

    return render_template('third.html', title = _title, content = _content)

@app.route('/dashboard/')

def dashboard() :

    df = pd.read_csv('../csv/corona.csv')

    # 컬럼의 이름을 변경
    df.columns = ['인덱스', '등록일시', '사망자', '확진자',
                  '게시글번호', '기준일', '기준시간', '수정일시',
                  '누적의심자', '누적확진률']

    # 등록일시를 기준으로 오름차순 정렬
    df.sort_values('등록일시', inplace = True)

    # '일일확진자', '일일사망자'라는 파생변수 생성
    df['일일확진자'] = df['확진자'] - df['확진자'].shift()
    df['일일사망자'] = df['사망자'].diff()

    data = df.head(15)

    cnt = len(data)

    dead_data = data['일일사망자'].tolist()

    decide_data = data['일일확진자'].tolist()
    
    date_list = data['등록일시'].tolist()

    return render_template('dashboard.html',
                            cnt = cnt, date_list = date_list,
                            decide_data = decide_data, dead_data = dead_data
                            )


# Flask라는 Class 안에 있는 run()이라는 함수 호출
app.run()

# 실제 서버와 유저간의 데이터의 이동
# 딕셔너리 형태의 데이터로 request / response
# request → 유저가 서버에게 보내는 데이터
# response → 서버가 유저에게 보내는 데이터
# request = {
#            key : value,
#            key2, value2,
#            ...,
#            args : {
#                   ID : input에서 입력한 값(ID), password : input에서 입력한 값(password)
#                   }
#           }
# request['args']['ID'] == request.args.get('ID')

# "GET / HTTP/1.1" 200 -: 200은 성공했다는 의미
# 주소 설정할 때 맨 뒤에 '/'를 붙여주는게 좋다.
