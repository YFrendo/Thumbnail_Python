Evaluation Python Yann Frendo SIO 2020

##################  Démarage de l'ap web    ###########################
Pour lancer l'app web:
Après avoir installé tout les packages requis dans le fichier requirement.txt

Lancer le serveur flask : 'FLASK_APP=serveur_flask.py flask run
Vérifier que le serveur est lancer sur: http://127.0.0.1:5000/
Sinon cf.serveur_flask.py/task_celery.py
Le lancer dans le dossier eval_python

Lancer le serveur redis: 
Exemple avec docker: docker run --name exemple-redis -d -p 6379:6379 redis
Si redis n'est pas lancé sur docker faire attention à bien le monter sur les
ports 6379 sinon se référer à la documentation

Lancer celeris: celery -A task_celery worker --loglevel=info
Le lancer dans le dossier eval_python

Voila tout est pret!
On peut avoir des information en allant sur la page:
http://127.0.0.1:5000/

Pour faire un test on peut utiliser le fichier test cf test.py
Sinon manuellement prendre une image puis avec curl:
curl -F "file=@#url_vers_l'image" http://127.0.0.1:5000/images
Le serveur renvoi le numéro d'ID de l'image.

On peut accéder sur son navigateur web via les URL:
http://127.0.0.1:5000/images/<id> 
Donnes les métadonnées et un lien vers la vignette si la création
c'est biendéroulé

Le lien vers la vignette est de la forme:
http://127.0.0.1:5000/vignette/<id>
Ce lien affiche la vignette si la création c'est bien passé!

################## Fonctionnement global ###############################

Lors de l'Upload l'ap va vérifier que il y a un bien un fichier envoyé 
et que celui ci est bien une image.

L'ap va ensuite créer un dossier avec le numéro d'ID de l'image
(cette ID est le numéro d'arrivé de l'image en commencant à 0)

Dans ce dossier il sera stocké l'image et les futur métadonné anssi que la
vignette.

Les métadonné sont extraite durant la phase d'upload et stocké dans un fichier 
texte dans le dossier de l'image

La création de la vignette est confié à un "serveur" celery qui va ensuite la stocké
dans le dossier. 
Au vu du temps d'éxécution de la création de la vignette cella n'était peut etre pas nécéssaire
mais bon pour la beauté du geste...


##################  Fichier serveur_flask.py ###########################

C'est le fichier de configuration du serveur flask

Si l'URL du serveur flask n'est pas: http://127.0.0.1:5000/ il faut 
modifier la ligne 'HOST' avec la bonne URL

On peut également modifier le fichier d'enregistrement des images
et des vignettes en modifiant les lignes UPLOAD_FOLDER et HTML_PATH
par défault : './static/uploads/'

Attention si le fichier n'est pas stocké dans static il faut modifier
la configuration du serveur flask sinon il va y avoir des problématiques
d'affichage de la vignette. (cf static folder flask)

###################  Fichier task_celery.py:  #########################
C'est le fichier de configuration de celery pour les taches asynchrone.

Il faut modifier la ligne UPLOAD_FOLDER en cas de changement de fichier
 d'enregistrement par défault: './static/uploads/'

Il faut également modifier la ligne 4 en modifiant borker si l'adresse
 du serveur redis n'est pas: 'redis://guest@localhost:6379//'
################### Fichier test.py/Dossier image_test  ################

Fichier exécutable avec pytest et qui permet d'effectuer une suite de 
test vérifiant le bon fonctionnement du serveur

Fonctionne avec le dossier image_test qui contient une image (un image pris
avec mon téléphone pour avoir des métadonnées) et un fichier texte.

################### Dossier templates ###################################

Contient les templates HTML pour l'affichage des pages web

################### Critiques et amélioration possibles #################

Les métadonnées ne sont pas au format JSON car il y a des problèmes avec 
certaines données qui sont au format bytes (mais pas toute) ce qui
nécéssiterai la création d'une solution de tri.

Certaines erreur pourrait etre mieux indiqué (peut etre avec le retour de
code d'erreurs)

Trouver une solution pour faire un fichier de configuration global pour ne
pas avoir à jongler entre les fichiers

Faire une base de donnée au lieu de fichier static

Rajouter des options comme une fonction de download du fichier ect...

Mais bon si je me lance dans tout ca j'ai plus le temps pour le reste et 
comme ca fonctionne acctuelement voila!

Bon courage pour la correction!
(PS : Je conseille de jeter un oeil à l'image test ;) )
