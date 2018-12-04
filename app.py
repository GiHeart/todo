from flask import Flask, render_template, url_for, request, redirect, make_response
from pymongo import MongoClient
from datetime import datetime
import time

app = Flask(__name__)
client = MongoClient()
db = client['todo']
collection = db['content']


@app.route('/')
def index():
    return render_template('sign_in.html')


@app.route('/testa')
def testa():
    cookie = request.cookies
    if cookie:
        x = cookie['username']
        print(x)
        collection = db[f'{x}']
        data = collection.find({}).sort([('status', 1)])
        return render_template('aftersign.html', data=data, user=x)
    else:
        collection = db['content']
        data = collection.find({}).sort([('status', 1)])
        return render_template('index.html', data=data)


@app.route('/get')
def get():
    return 'Hello World!'


@app.route('/add', methods=['GET', 'POST'])
def add():
    cookie = request.cookies
    if request.method == 'GET':
        if cookie:
            user = cookie['username']
            return render_template('afteradd.html', user=user)
        else:
            return render_template('add.html')
    else:
        content = request.form
        u_content = content['u_content']
        print(u_content)
        if cookie:
            user = cookie['username']
            collection = db[f'{user}']
            collection.insert_one({'content': u_content, 'create_time': datetime.now(), 'status': 0, 'finish_time': '', 'time': time.time()})
            return redirect(url_for('testa'))
        else:
            collection = db['content']
            collection.insert_one({'content': u_content, 'create_time': datetime.now(), 'status': 0, 'finish_time': '', 'time': time.time()})
            return redirect(url_for('testa'))


@app.route('/finish')
def finish():
    cookie = request.cookies
    if cookie:
        user = cookie['username']
        collection = db[f'{user}']
        args = request.args
        id = args['id']
        print(id)
        collection.update({'content': id}, {'$set': {'status': 1, 'finish_time': datetime.now()}})
        return redirect(url_for('testa'))
    else:
        collection = db['content']
        args = request.args
        id = args['id']
        print(id)
        collection.update({'content': id}, {'$set': {'status': 1, 'finish_time': datetime.now()}})
        return redirect(url_for('testa'))


@app.route('/delete')
def delete():
    cookie = request.cookies
    args = request.args
    time = args['id']
    if cookie:
        user = cookie['username']
        collection = db[f'{user}']
        collection.delete_one({'content': time})
        return redirect(url_for('testa'))
    else:
        collection = db['content']
        collection.delete_one({'content': time})
        return redirect(url_for('testa'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'GET':
        args = request.args
        global x
        x = args['id']
        print(x)
        return render_template('update.html', a=x)
    else:
        cookie = request.cookies
        form = request.form
        con = form['modify']
        if cookie:
            user = cookie['username']
            collection = db[f'{user}']
            collection.update({'content': x}, {'$set': {'content': con}})
            print(con)
            return redirect(url_for('testa'))
        else:
            collection = db['content']
            collection.update({'content': x}, {'$set': {'content': con}})
            print(con)
            return redirect(url_for('testa'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if request.method == 'GET':
        return render_template('sign_in.html')
    else:
        form = request.form
        user = form['user']
        password = form['password']
        print(user)
        print(password)
        collection = db['user']
        a = collection.find_one({'user': user})
        if user == a['user'] and password == a['password']:
            collection = db[f'{user}']
            data = collection.find({})
            resonse = make_response(render_template('aftersign.html', user=user, data=data))
            print(user)
            resonse.set_cookie('username', user)
            resonse.set_cookie('password', password)
            return resonse
        else:
            return '用户名或密码输错'


@app.route('/delete_cookie')
def delete_cookie():
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('username')
    response.delete_cookie('password')
    return response


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html')
    else:
        form = request.form
        username = form['username']
        password = form['password']
        collection = db['user']
        collection.insert_one({'user': username, 'password': password})
        return render_template('sign_in.html')


if __name__ == '__main__':
    app.run()
