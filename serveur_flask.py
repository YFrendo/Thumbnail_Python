import os
from flask import Flask,flash,request,redirect,url_for, jsonify
from PIL import Image, ExifTags
from task_celery import vignette

UPLOAD_FOLDER = './uploads'
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

        filename, ext  = os.path.splitext(upload_file.filename)
        im.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/' + id_dossier, upload_file.filename)) 

        exif = {
                ExifTags.TAGS[k] : v
                for k, v in im.getexif().items()
                if k in ExifTags.TAGS
                }
        exif = str(exif)
        with open('./uploads/' + id_dossier + '/metadata.json','w') as outfile:
            outfile.write(exif)

        vignette.delay(id_dossier,upload_file.filename)
        return id_dossier 

@app.route('/images/<id_photo>')
def image(id_photo):

    with open('./uploads/' + id_photo + '/metadata.json','r') as outfile:
        texte = outfile.read()
        texte = str(texte) + '<br>'

    if os.path.isfile('./uploads/' + id_photo + '/thumbnail.jpg'):
        texte = texte + 'Thumbnail succes <br>'
        texte = texte + 'http://127.0.0.1:5000/thumbnail/' + id_photo
        return(texte)
    elif os.path.isfile('./uploads/' + id_photo + '/fail'):
        texte = texte + 'Echec création vignette'
        return(texte)
    texte = texte + 'Vignette en création'
    return(texte)

@app.route('/thumbnail/<id_photo>')
def thumbnail(id_photo):

    if os.path.isfile('./uploads/' + id_photo + '/thumbnail.jpg'):
        thumbnail = './uploads/' + id_photo + '/thumbnail.jpg'
        return('<img src="' + thumbnail +'">')
    else:
        return('Pas de vignette')



