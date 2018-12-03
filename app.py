from flask import Flask, render_template, url_for
from pymongo import MongoClient

app = Flask(__name__)
# client = MongoClient()
# db = client['todo']
# collection = db['']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get')
def hello_world1():
    return 'Hello World!'


@app.route('/add')
def hello_world2():
    return 'Hello World!'


@app.route('/finish')
def hello_world3():
    return 'Hello World!'


@app.route('/delete')
def hello_world4():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
