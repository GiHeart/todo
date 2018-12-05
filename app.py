from flask import Flask, render_template, url_for, request, redirect, make_response
from pymongo import MongoClient
from datetime import datetime
import time
from bson import ObjectId

app = Flask(__name__)
# 连接数据库
client = MongoClient()
db = client['todo']
collection = db['content']


@app.route('/')
def index():
    """返回登录页面"""
    return render_template('sign_in.html')


@app.route('/testa')
def testa():
    cookie = request.cookies  # 接收cookie
    if cookie:
        # 如果有cookie就是已登录状态
        x = cookie['username']
        print(x)
        # 切换数据库集合，让不同用户操作
        collection = db[f'{x}']
        data = collection.find({}).sort([('status', 1), ('time', 1)])

        # 返回登录后的页面
        return render_template('aftersign.html', data=data, user=x)
    else:
        # 如果没有cookie则返回index.html
        collection = db['content']
        data = collection.find({}).sort([('status', 1), ('time', 1)])
        return render_template('index.html', data=data)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """添加todo记录，接收两种请求，GET请求返回add.html页面，同样使用cookie来判断用户登录状态返回不同的页面"""
    cookie = request.cookies
    if request.method == 'GET':
        if cookie:
            user = cookie['username']
            return render_template('afteradd.html', user=user)
        else:
            return render_template('add.html')
    else:
        """提交后返回testa路由"""
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
    """更改状态为已完成"""
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
    """删除记录"""
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
    """更新内容"""
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
    """about页面"""
    return render_template('about.html')


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    """用户登录"""
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
            data = collection.find({}).sort([('status', 1)])
            resonse = make_response(render_template('aftersign.html', user=user, data=data))
            print(user)
            resonse.set_cookie('username', user)
            # resonse.set_cookie('password', password)
            return resonse
        else:
            return '用户名或密码输错'


@app.route('/delete_cookie')
def delete_cookie():
    """用户注销，删除cookie"""
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('username')
    # response.delete_cookie('password')
    return response


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    """用户注册"""
    if request.method == 'GET':
        return render_template('sign_up.html')
    else:
        form = request.form
        username = form['username']
        password = form['password']
        collection = db['user']
        collection.insert_one({'user': username, 'password': password})
        return render_template('sign_in.html')


@app.route('/comment', methods=['GET', 'post'])
def comment():
    cookie = request.cookies
    if request.method == 'GET':
        if cookie:
            user = cookie['username']
            collection = db['comment']
            comment_data = collection.find({})
            return render_template('aftercomment.html', comment_data=comment_data, user=user)
        else:
            collection = db['comment']
            comment_data = collection.find({})
            return render_template('comment.html', comment_data=comment_data)
    else:
        if cookie:
            user = cookie['username']
            form = request.form
            text = form['text']
            collection = db['comment']
            collection.insert_one({'comment': text, 'comment_datetime': datetime.now(), 'user': user})
            return redirect(url_for('comment'))
        else:
            form = request.form
            text = form['text']
            collection = db['comment']
            collection.insert_one({'comment': text, 'comment_datetime': datetime.now(), 'user': '未登录用户'})
            return redirect(url_for('comment'))


@app.route('/management')
def management():
    collection = db['comment']
    comment_data = collection.find({})
    return render_template('Management_review.html', comment_data=comment_data)


@app.route('/delete_comment')
def delete_comment():
    arg = request.args
    id = arg['id']
    _id = ObjectId(id)
    collection = db['comment']
    collection.delete_one({'_id': _id})
    return redirect(url_for('management'))


if __name__ == '__main__':
    app.run()
