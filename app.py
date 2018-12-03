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


@app.route('/add', methods=['POST'])
def add():
    content = request.form
    u_content = content['u_content']
    print(u_content)
    collection.insert_one({'content': u_content, 'create_time': datetime.now(), 'status': 0, 'finish_time': None, 'time': time.time()})
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
    collection.update({'content': id}, {'$set': {'status': 1}})
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


if __name__ == '__main__':
    app.run()
