from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient
from datetime import datetime
import time

app = Flask(__name__)
client = MongoClient()
db = client['todo']
collection = db['content']


@app.route('/')
def index():
    return redirect('testa')


@app.route('/testa')
def testa():
    data = collection.find({})
    return render_template('index.html', data=data)


@app.route('/get')
def get():
    return 'Hello World!'


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        content = request.form
        u_content = content['u_content']
        print(u_content)
        collection.insert_one({'content': u_content, 'create_time': datetime.now(), 'status': 0, 'finish_time': '', 'time': time.time()})
        x = collection.find_one({})
        print(x)
        if x:
            time.sleep(2)
            return redirect(url_for('index'))


@app.route('/finish')
def finish():
    args = request.args
    id = args['id']
    print(id)
    collection.update({'content': id}, {'$set': {'status': 1, 'finish_time': datetime.now()}})
    return redirect(url_for('index'))


@app.route('/delete')
def delete():
    args = request.args
    time = args['id']
    # x = float(time)
    # print(type(time))
    print(type(time))
    collection.delete_one({'content': time})
    return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'GET':
        args = request.args
        global x
        x = args['id']
        print(x)
        return render_template('update.html', a=x)
    else:
        form = request.form
        con = form['modify']
        collection.update({'content': x}, {'$set': {'content': con}})
        print(con)
        return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if request.method == 'GET':
        return render_template('sign.html')
    else:
        form = request.form
        user = form['user']
        password = form['password']
        print(user)
        print(password)
        collection = db['user']
        a = collection.find_one({'user': user})
        print(a)
        if user == a['user'] and password == a['password']:
            return '登录成功'
        else:
            return '用户名或密码输错'


if __name__ == '__main__':
    app.run()
