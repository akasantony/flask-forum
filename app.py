#!/usr/bin/python

__authors__ = "Akas Antony"
__email__ = "antony.akas@gmail.com"
__date__ = "27th, October 2015"

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__, static_url_path='')
client = MongoClient()
db = client.Forum

def get_featured_results():
    
    posts = list(reversed(list(db.posts.find())))
    posts = posts[:5]
    print(posts)
    return posts


@app.route('/', methods = ['GET'])
def index():
    if request.method == 'GET':
        results = get_featured_results()
        return render_template('index.html', results=results)

@app.route('/browse', methods = ['GET','POST'])
def browse():
    if request.method == 'GET':
        posts = reversed(list(db.posts.find()))
        print(posts)
        return render_template('browse.html', results=posts)

@app.route('/about', methods = ['GET'])
def about():
    if request.method == 'GET':
        return render_template('about.html')

@app.route('/ask', methods = ['POST', 'GET'])
def post():
    if request.method == 'GET':
        return render_template('ask.html')
    if request.method == 'POST':
        question = request.form['question']
        print (question)
        post_query = {'question': question}
        print(post_query)
        posts = db.posts
        posts.insert_one(post_query)
        return render_template('ask.html')

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)


@app.route('/<id>', methods = ['GET', 'POST'])
def show_discussion(id):
    if request.method == 'GET':
        post = db.posts.find_one({'_id': ObjectId(id)})
        return render_template('discuss.html', result = post)

    if request.method == 'POST':
        answer = request.form['answer']
        db.posts.update({'_id': ObjectId(id)}, { '$push': {'answer': answer} })
        post = db.posts.find_one({'_id': ObjectId(id)})
        return render_template('discuss.html', result = post)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
