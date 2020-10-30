import json
import os
import uuid
from flask import Flask,flash,request,redirect,url_for
from werkzeug.utils import secure_filename
from PIL import Image


UPLOAD_FOLDER = './uploads'
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
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        upload_file = request.files['file']

        if upload_file.filename == '':
            return 'No selected file'
        
        try:
           im = Image.open(upload_file)
        except:
            return "Cannot open file"

        filename = str(len(os.listdir('./uploads'))) #Donne un numéroID unique
        upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename 



