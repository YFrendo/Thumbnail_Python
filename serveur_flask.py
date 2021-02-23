import os
from flask import Flask,flash,request,redirect,url_for,  render_template
from PIL import Image, ExifTags
from task_celery import vignette

UPLOAD_FOLDER = './static/uploads/'
HTML_PATH  = '/static/uploads'
HOST = 'http://127.0.0.1:5000'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['HOST'] = HOST
app.config['HTML_PATH'] = HTML_PATH

@app.route('/')
def bienvenue():#Page avec information
    return(render_template("First_page.html"))


@app.route('/images',methods=['GET','POST'])
#Enregistre l'image et extrait les métadonnés
def upload():

    if not os.path.isdir(app.config['UPLOAD_FOLDER']): #Vérifie l'existance du fichier pour enregistrer les images
        os.makedirs(app.config['UPLOAD_FOLDER'])#Le cas échéant le créé

    if request.method == 'POST':#Vérifie l'existance d'un fichier dans la requete POST
        if 'file' not in request.files:
            return 'No file part'
        upload_file = request.files['file']

        if upload_file.filename == '':#Si il y a pas de de fichier ca crash ici
            return 'No selected file'
        
        try:#Si le fichier n'est pas une image ca crash ici
           im = Image.open(upload_file)
        except:
            return "Cannot open file"
        #Donne un numéroID unique correspondant à son ordre d'arrivé (commence à 0)
        id_dossier = str(len(os.listdir(app.config['UPLOAD_FOLDER']))) 
        os.makedirs(app.config['UPLOAD_FOLDER'] + id_dossier)#Fait un dossier avec le numéro d'id

        filename, ext  = os.path.splitext(upload_file.filename) #Permet d'enlever l'extension du fichier
        im.save(os.path.join(app.config['UPLOAD_FOLDER'] + id_dossier, upload_file.filename))#Enregistre l'image 
        
        #Permet d'extraire les métadonné et les écris dans un fichier 
        exif = { 
                ExifTags.TAGS[k] : v
                for k, v in im.getexif().items()
                if k in ExifTags.TAGS
                }
        exif = str(exif)
        with open(app.config['UPLOAD_FOLDER'] + id_dossier + '/metadata.txt','w') as outfile:
            outfile.write(exif)
        
        vignette.delay(id_dossier,upload_file.filename) #Donne la création de la vignette a celery
        return id_dossier 

@app.route('/images/<id_photo>')
def image(id_photo):
    
    if not os.path.isdir(app.config['UPLOAD_FOLDER'] + id_photo): #Vérifie que il y a bien une photo à cette id
        return("Pas de photo à cette ID")
    try:
        with open(app.config['UPLOAD_FOLDER'] + id_photo + '/metadata.txt','r') as outfile:#Affiche les métadonné
            texte = outfile.read()
            texte = str(texte) + '<br>'
    except:#En cas de problème
        texte = "Problème extraction métadonnées<br>"

    if os.path.isfile(app.config['UPLOAD_FOLDER'] + id_photo + '/thumbnail.jpg'):#Si la vignette est bien créé
        texte = texte + 'Thumbnail succes <br>'
        texte = texte + app.config['HOST'] + '/vignette/' + id_photo
        return(texte)
    elif os.path.isfile(app.config['UPLOAD_FOLDER'] + id_photo + '/fail'):#Si il y a eu un problème lors de la création
        texte = texte + 'Echec création vignette'
        return(texte)
    texte = texte + 'Vignette en création'#SI elle est pas encore créé
    return(texte)

@app.route('/vignette/<id_photo>')
def thumbnail(id_photo):

    if os.path.isfile(app.config['UPLOAD_FOLDER'] + '/'+  id_photo + '/thumbnail.jpg'):#Vérifie que la vignette existe bien
        full_filename = os.path.join(app.config['HTML_PATH'] + '/' + id_photo, 'thumbnail.jpg') 
        return(render_template("vignette.html", user_image = full_filename ))#L'affiche via le template html 
    else:
        return('Pas de vignette') #Si il n'y a pas de vignette




