from flask import Flask, render_template 
from redis import StrictRedis

from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)


db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    age = db.Column(db.Integer, unique=True)

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return '<User %r>' % self.name


@app.route('/', methods=['GET', 'POST'])
def index():
    stu = Student('jet Li', 59)
    db.session.add(stu)
    db.session.commit()

    print('12345')
    r= None 
    try:
        r = StrictRedis(host='redis01',decode_responses=True)
        if not r.get("k1"):
            r.set("k1",0)
        r.incr("k1")
        return render_template('index.html', num = r.get("k1"))
    finally:
        r.close()
