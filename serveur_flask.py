import json
import os
from flask import Flask
from flask import jsonify

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf','png','jpg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def bienvenue():
    with open('first_page.txt', 'r') as file:
            data = file.read()
    return(data)


@app.route('/images',methods=['GET','POST'])
def upload():
    if request


