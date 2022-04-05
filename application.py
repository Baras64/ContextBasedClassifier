from flask import Flask, render_template, request
import model_load
import json
from passlib.hash import pbkdf2_sha256
import string
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import random

engine = create_engine('postgres://postgres:toor@localhost/Baras')
db = scoped_session(sessionmaker(bind=engine))


app = Flask(__name__, static_folder='templates/assets')
API_KEY_LENGTH = 7
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    email_id = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    api_key = generate_api_key()
    if confirm_password == password:
        password = hashing(password)
        query = "INSERT INTO login_credentials (email_id, password, api_key) VALUES (:email_id, :password, :api_key)"
        db.execute(query, {"email_id": email_id, "password": password, "api_key": api_key})
        db.commit()
        return render_template('login.html')
    return render_template('signup.html')

global_api  = 0

@app.route('/check_data', methods=['POST'])
def check_data():
    password = request.form['password']
    email_id = request.form['email_id']
    if check_hashing(email_id, password):
        get_api = db.execute(f"SELECT * FROM login_credentials WHERE email_id='{email_id}';").fetchall()
        model_load.api = get_api[0][3]
        return render_template('index.html', API_KEY= model_load.api)
    return render_template('login.html')

@app.route('/api/<string:api_key>/<string:text_to_predict>')
def json_return(api_key, text_to_predict):
    query = f"SELECT api_key FROM login_credentials WHERE api_key='{api_key}';"
    api = db.execute(query).fetchall()
    print(api)
    if len(api) == 0:
        print('debug')
        err_dict = {'error': 'Invalid API key'}
        return json.dumps(err_dict)
    obj = model_load.Model()
    predicted = obj.predicton(text_to_predict)
    dict = {}
    dict['text'] = text_to_predict

    if predicted > 0.5:
        dict['label'] = 1
        dict['prediction'] = str(predicted[0][0])
        dict['predicted_text'] = "From the If-Else Chapter"
    else:
        dict['label'] = 0
        dict['prediction'] = str(predicted[0][0])
        dict['predicted_text'] = "NOT From the If-Else Chapter"

    return json.dumps(dict)

def hashing(password):
    return pbkdf2_sha256.hash(password, rounds=1000, salt=b'Baras')

def check_hashing(email_id, password):
    query = f"SELECT * FROM login_credentials WHERE email_id='{email_id}';"
    users = db.execute(query).fetchone()
    if users == None:
        return False
    else:
        if pbkdf2_sha256.verify(password, users.password):
            return True
        else:
            return False

@app.route('/predict_text', methods=['POST'])
def predict_text():
    text = request.form['sentiment_text']
    obj = model_load.Model()
    predicted_text=obj.predicton(text)
    if predicted_text > 0.5:
        return render_template('index.html', response="It is an if else statement", API_KEY=model_load.api)
    return render_template('index.html', response="not an if else statement", API_KEY=model_load.api)

def generate_api_key():
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=API_KEY_LENGTH))
    print(res)
    return res

if __name__ == '__main__':
    #
    # hashed = hashing('nayan123')
    # print(hashed)
    # print()
    app.run(debug=True)