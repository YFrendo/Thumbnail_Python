import json
import os
import pickle
from flask import Flask,flash,request,redirect,url_for
from werkzeug.utils import secure_filename
from PIL import Image, ExifTags
from task_celery import extract_metadata

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

        id_dossier = str(len(os.listdir('./uploads'))) #Donne un numéroID unique
        os.makedirs('./uploads/' + id_dossier)#Fait un dossier avec le numéro d'id
        im.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/' + id_dossier, upload_file.filename)) 

        exif = {
                ExifTags.TAGS[k] : v
                for k, v in im.getexif().items()
                if k in ExifTags.TAGS
                }
        exif = str(exif)
        print(type(exif))
        print(exif)
        with open('./uploads/' + id_dossier + '/' + upload_file.filename + '_metadata.json','w') as outfile:
            outfile.write(exif)
        #Enregistre le fichier dans le dossier
        return id_dossier 



