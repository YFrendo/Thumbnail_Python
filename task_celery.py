from celery import Celery
from PIL import Image, ExifTags
import json
app = Celery('tasks' , broker = 'redis://guest@localhost:6379//')
UPLOAD_FOLDER = './static/uploads/'

@app.task
def vignette(id_doc,image_name):
    try:#Procède à la création d'une vignette
        im = Image.open(UPLOAD_FOLDER + id_doc + "/" + image_name)
        im.thumbnail((50,50))
        r,g,b,*args = im.split()
        im = Image.merge("RGB", (r,g,b))
        im.save(UPLOAD_FOLDER + id_doc + "/thumbnail.jpg","JPEG")
    except:#En cas d'echec créer un fichier fail qui informe de l'échec
        fichier = open(UPLOAD_FOLDER + id_doc + "/fail", "r")
        fichier.close()

