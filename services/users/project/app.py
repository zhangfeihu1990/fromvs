from flask import Flask, render_template ,jsonify
from redis import StrictRedis
from flask_sqlalchemy import SQLAlchemy
import pymysql
import json


pymysql.install_as_MySQLdb()

app = Flask(__name__)

baseURL = "mysql://root:123456@139.9.115.246:3306/test"
app.config['SQLALCHEMY_DATABASE_URI'] = baseURL #配置数据库url
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    age = db.Column(db.Integer, unique=False)

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return '<User %r>' % self.name

@app.route('/', methods=['GET', 'POST'])
def index():
    print('12345')
    r= None 
    try:
        r = StrictRedis(host='139.9.115.246',port=6380,decode_responses=True)
        if not r.get("k1"):
            r.set("k1",0)
        r.incr("k1")
        return render_template('index.html', num = r.get("k1"))
    finally:
        r.close()

@app.route('/add', methods=['GET', 'POST'])
def add():
    print('test....')
    stu = Student('jet Li', 58)
    db.session.add(stu)
    db.session.commit() 
    return "add sucess!"

@app.route('/query', methods=['GET', 'POST'])
def query():
    print('test..query..')
    stulist  = Student.query.first()
    print('test..query..end')
    return jsonify({
    'status': 'success',
    'message': stulist
     })
    

if __name__ == '__main__':
    app.run()
