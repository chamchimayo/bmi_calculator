from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

SECRET_KEY = 'SPARTA'

client = MongoClient('mongodb+srv://sparta:sparta@cluster0.15mplrd.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta



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

    now = datetime.today()

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

@app.route('/bmi_check')
def user_bmi():
    user_num = int(request.args.get("user_num"))
    user = db.user.find_one({'num':user_num})
    bmi_list = list(db.user_bmi.find({'user_num':user_num}, {'_id': False}).sort([("user_bmi_num", -1)]))
    bmi_data = bmi_list[0]['user_bmi']

    return render_template('userBmi.html', user_num=user_num, user=user, bmi_list=bmi_list, bmi_data=bmi_data)

@app.route("/api/bmi_check", methods=["GET"])
def bmi_get():
    args = request.args
    user_bmi_num = int(args.get('user_bmi_num'))

    bmi = db.user_bmi.find_one({'user_bmi_num': user_bmi_num})
    user_hegit = bmi["user_height"]
    user_weight = bmi["user_weight"]
    user_bmi_value = bmi["user_bmi"]

    user_bmi_info = [user_hegit, user_weight, user_bmi_value]

    return user_bmi_info


def format_datetime(value, format=None):
  if format is None:
    weekdays = ['월', '화', '수', '목', '금', '토', '일']
    wd = weekdays[value.weekday()]
    format = "%Y년 %m월 %d일 ({})".format(wd)
    formatted = value.strftime(format.encode('unicode-escape').decode()).encode().decode('unicode-escape')
  else:
    formatted = value.strftime(format.encode('unicode-escape').decode()).encode().decode('unicode-escape')
  return formatted

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
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'id': username_receive, 'pw': pw_hash})
    print(result)

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')#.decode('utf-8')
        name = result['name']

        return jsonify({'result': 'success', 'token': token, 'name':name})

    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
