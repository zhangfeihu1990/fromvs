from flask import Flask, render_template ,jsonify
from redis import StrictRedis
from flask_sqlalchemy import SQLAlchemy
import pymysql
import json
#pour csv
from flask import Response
from flask import stream_with_context
from io import StringIO
import csv


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
    #return stulist
    return jsonify({
    'status': 'success',
    'message': stulist.name
     })

@app.route('/hello/<userid>/', methods=['GET', 'POST'])
def hello(userid):
    print('id..{}'.format(userid))
    user  = Student.query.filter_by(id=userid).first()
    print('test..query..end')

    return render_template('hello.html', name = user.name)   

#	测试数据
data = [
		['Jack','jack@abc.com'],
		['Ben','ben@abc.com'],
		['jerry','jerry@abc.com']
	]


@app.route('/api/exportEmails', methods=['GET'])
def exportEmails():
	#	定义一个生成器 (generate)，逐行生成，实现流式传输
    def generate():
    	#	用 StringIO 在内存中写，不会生成实际文件
        io = StringIO()	#在 io 中写 csv
        w = csv.writer(io)
        for i in data:      #对于 data 中的每一条
            w.writerow(i)   #传入的是一个数组 ['xxx','xxx@xxx.xxx'] csv.writer 会把它处理成逗号分隔的一行
            				#需要注意的是传入仅一个字符串 '' 时，会被逐字符分割，所以要写成 ['xxx'] 的形式
            yield io.getvalue()		#返回写入的值
            io.seek(0)		#io流的指针回到起点
            io.truncate(0)	#删去指针之后的部分，即清空所有写入的内容，准备下一行的写入
    #	用 generate() 构造返回值
    response = Response(stream_with_context(generate()), mimetype='text/csv')
    #	设置Headers: Content-Disposition: attachment 表示默认会直接下载。 指定 filename。
    response.headers.set("Content-Disposition","attachment",filename="emails.csv")
    #	将 response 返回
    return response

@app.route('/api/generfil', methods=['GET'])
def readDiskfile():
    file_object = open("d:/2.txt",encoding="gbk").read()
    f3 = open("d:/3.txt","a")
    # 获取当前的文件偏移，由于还没开始读取内容，偏移量等于 0
    #count = file_object.tell()
    #print(count)
    # 读取文本所有数据内容，文件自动偏移到文件末尾
    #contents = file_object.read()
    # 获取整个文件的偏移量 ,实际上就是文件内容的大小
    #count = file_object.tell()
    #print(count)
    for content in file_object:
    # 将文件指针偏移到文件开始位置
        #file_object.seek(0,0)
    # 读取一行数据，按道理讲应该是获取第一行数据
        #c = file_object.readline()
        print(content)
        f3.write(content)
        
    #file_object.close()
    f3.close

    return "ok"

if __name__ == '__main__':
    app.run()
