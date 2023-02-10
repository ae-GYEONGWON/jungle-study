from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.gw  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/post', methods=['POST'])
def post_memo():
   title_receive = request.form['title_give']  
   text_receive = request.form['text_give']
   now_data = list(db.memos.find({}))
   if len(now_data) == 0:
      num_receive = '1'
   else:
      num_receive = str(now_data[-1]['card_num'] + 1)

   memo = {'title': title_receive, 'text': text_receive, 'card_num': num_receive}
   db.memos.insert_one(memo)

   return jsonify({'result': 'success'})

@app.route('/memo/delete', methods=['POST'])
def delete_memo():
   num_receive = request.form['num_give']
   db.memos.delete_one({'card_num': num_receive})
   return jsonify({'result': 'success'})

@app.route('/memo/mod', methods=['POST'])
def mod_memo():
   mod_title_receive = request.form['mod_title_give']
   mod_text_receive = request.form['mod_text_give']
   num_receive = request.form['num_give']
   
   db.memos.update_one({'card_num':num_receive}, {'$set':{'text':mod_text_receive}})
   db.memos.update_one({'card_num':num_receive}, {'$set':{'title':mod_title_receive}})
   return jsonify({'result': 'success'})


@app.route('/memo', methods=['GET'])
def read_memos():
    result = list(db.memos.find({}, {'_id': 0}).sort('card_num'))
    return jsonify({'result': 'success', 'memos': result})
if __name__ == '__main__':    app.run('0.0.0.0', port=5000, debug=True)