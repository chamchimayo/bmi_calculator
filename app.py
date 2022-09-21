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





@app.route('/')  #1
def home():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload["id"]})
        user_num_receive = int(user_info["num"])
        print("user_num_receive", user_num_receive)

        return render_template('index.html', user_num=user_num_receive)


    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))




@app.route("/bmi_register", methods=["POST"])  #1-1
def bmi_register():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload["id"]})
        user_num_receive = user_info["num"]
        print("user_num_receive", user_num_receive)

        bmi_list = list(db.user_bmi.find({}, {'_id': False}))
        count = len(bmi_list) + 1

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
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("login", msg='로그인 정보가 존재하지 않습니다.'))


@app.route('/bmi_check') #2
def user_bmi():
    token_receive = request.cookies.get('mytoken')
    user_num = int(request.args.get("user_num"))
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        if user_num == payload["num"]:
            user = db.user.find_one({'num': user_num})
            bmi_list = list(db.user_bmi.find({'user_num': user_num}, {'_id': False}).sort([("user_bmi_num", -1)]))
            bmi_data = bmi_list[0]['user_bmi']
            return render_template('userBmi.html', user_num=user_num, user=user, bmi_list=bmi_list, bmi_data=bmi_data)
        else:
            return redirect(url_for("home", msg="유저 불일치 열람불가"))
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home", msg="로그인 정보가 존재하지 않습니다."))





@app.route("/api/bmi_check", methods=["GET"]) #2-1
def bmi_get():
    args = request.args
    user_bmi_num = int(args.get('user_bmi_num'))

    bmi = db.user_bmi.find_one({'user_bmi_num': user_bmi_num})
    user_hegit = bmi["user_height"]
    user_weight = bmi["user_weight"]
    user_bmi_value = bmi["user_bmi"]

    user_bmi_info = [user_hegit, user_weight, user_bmi_value]

    return user_bmi_info


@app.route('/login') #3
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/api/login', methods=['POST']) #3-1
def api_login():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'id': username_receive, 'pw': pw_hash})
    num = result['num']
    print(result)

    if result is not None:
        payload = {
            'num': num,
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60*60*24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')#.decode('utf-8')
        name = result['name']

        return jsonify({'result': 'success', 'token': token, 'name':name})

    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/register') #4
def register():
    return render_template('register.html')


@app.route('/api/register', methods=['POST']) #4-1
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



@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    userid_receive = request.form['userid_give']
    exists = bool(db.user.find_one({"id": userid_receive}))
    return jsonify({'result': 'success', 'exists': exists})



def format_datetime(value, format=None):
  if format is None:
    weekdays = ['월', '화', '수', '목', '금', '토', '일']
    wd = weekdays[value.weekday()]
    format = "%Y년 %m월 %d일 ({})".format(wd)
    formatted = value.strftime(format.encode('unicode-escape').decode()).encode().decode('unicode-escape')
  else:
    formatted = value.strftime(format.encode('unicode-escape').decode()).encode().decode('unicode-escape')
  return formatted





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)