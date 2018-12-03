from flask import Flask, render_template, url_for, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
client = MongoClient()
db = client['todo']
collection = db['content']


# class Todo(object):
#     @staticmethod
#     def create_doc(self, content):
#         return{
#             'content': content,
#             'create_time': datetime.now(),
#             'status': 0,
#             'finish_time': None
#         }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get')
def hello_world1():
    return 'Hello World!'


@app.route('/add', methods=['POST'])
def add():
    content = request.form
    u_content = content['u_content']
    print(u_content)
    collection.insert_one({'content': u_content, 'create_time': datetime.now(), 'status': 0, 'finish_time': None})
    x = collection.find_one({})
    print(x)
    if x:
        return 'Hello World!'


@app.route('/finish')
def hello_world3():
    return 'Hello World!'


@app.route('/delete')
def hello_world4():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
