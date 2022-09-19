from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

# from pymongo import MongoClient
# client = MongoClient('mongodb+srv://test:sparta@cluster0.zslujo2.mongodb.net/Cluster0?retryWrites=true&w=majority')
# db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/login')
def login():
   return render_template('index.html')

@app.route('/join')
def join():
   return render_template('index.html')

@app.route('/userInput')
def user_input():
   return render_template('index.html')

def bmi_calculate(bmiCalculate):
   return render_template('index.html')


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)