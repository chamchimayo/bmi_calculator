from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://sparta:sparta@cluster0.15mplrd.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/bmi_register')
def bmi_register_form():
    return render_template('bmiRegister.html')


@app.route("/bmi_register", methods=["POST"])
def bmi_register():

    bmi_list = list(db.user_bmi.find({}, {'_id': False}))
    count = len(bmi_list) + 1

    user_num_receive = 1

    user_height_receive = request.form['user_height_give']
    user_weight_receive = request.form['user_weight_give']
    height_num = int(user_height_receive) / 100
    user_bmi = int(user_weight_receive) / (height_num * height_num)

    now = datetime.datetime.today()

    doc = {
        'user_bmi_num': count,
        'user_num': user_num_receive,
        'user_height': user_height_receive,
        'user_weight': user_weight_receive,
        'user_bmi': round(user_bmi, 2),
        'register_date': now
    }

    db.user_bmi.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})



@app.route('/index')
def main():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')


# ------------ API 구현 ------------------------

# 1. 회원가입: 회원가입 화면에서 '회원가입'버튼 클릭 시
@app.route('/api/register', methods=['POST'])
def api_register():
    name_receive = request.form['name_give']
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    mail_receive = request.form['name_give']
    userlist = list(db.user.find({}, {'_id': False}))
    count = len(userlist) + 1

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'name': name_receive, 'id': id_receive, 'pw': pw_hash, 'mail': mail_receive, 'num': count})

    return jsonify({'result': 'success'})

#1. 로그인: 로그인 화면에서 '로그인' 버튼 클릭 시
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.user_bmi.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10) # 잘되는지 확인 후 hour 단위로 변경
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
        # return render_template('index.html')

    else:
        return jsonify({'result':'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
