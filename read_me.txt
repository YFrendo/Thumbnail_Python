Évaluation Python Yann Frendo SIO 2020

##################  Démarrage de l'ap web    ###########################
Pour lancer l'app web:
Après avoir installé tous les packages requis dans le fichier requirement.txt

Lancer le serveur flask : 'FLASK_APP=serveur_flask.py flask run
Vérifier que le serveur est lancé sur: http://127.0.0.1:5000/
Sinon cf.serveur_flask.py/task_celery.py
Le lancer dans le dossier eval_python

Lancer le serveur redis: 
Exemple avec docker: docker run --name exemple-redis -d -p 6379:6379 redis
Si redis n'est pas lancé sur docker faire attention à bien le monter sur les
ports 6379 sinon se référer à la documentation

Lancer celeris: celery -A task_celery worker --loglevel=info
Le lancer dans le dossier eval_python

Voilà tout est prêt!
On peut avoir des informations en allant sur la page:
http://127.0.0.1:5000/

Pour faire un test, on peut utiliser le fichier test cf. test.py
Sinon manuellement prendre une image puis avec curl:
curl -F "file=@#url_vers_l'image" http://127.0.0.1:5000/images
Le serveur renvoie le numéro d'ID de l'image.

On peut accéder sur son navigateur web via les URL:
http://127.0.0.1:5000/images/<id> 
Donne les métadonnées et un lien vers la vignette si la création
c'est bien déroulé

Le lien vers la vignette est de la forme:
http://127.0.0.1:5000/vignette/<id>
Ce lien affiche la vignette si la création s'est bien passée!

################## Fonctionnement global ###############################

lors de l'Upload l'ap va vérifier qu’il y a un bien un fichier envoyé 
et que celui-ci est bien une image.

L'ap va ensuite créer un dossier avec le numéro d'ID de l'image
(cette ID est le numéro d'arrivé de l'image en commençant à 0)

Dans ce dossier il sera stocké l'image et les futures méthadones et la
vignette.

Les métadonnées sont extraites durant la phase d'upload et stockées dans un fichier 
texte dans le dossier de l'image

La création de la vignette est confiée à un "serveur" celery qui va ensuite la stocké
dans le dossier. 
Au vu du temps d'exécution de la création de la vignette cella n'était peut être pas nécessaire,
mais bon pour la beauté du geste...


##################  Fichier serveur_flask.py ###########################

C'est le fichier de configuration du serveur flask

Si l'URL du serveur flask n'est pas: http://127.0.0.1:5000/ il faut 
modifier la ligne 'HOST' avec la bonne URL

On peut également modifier le fichier d'enregistrement des images
et des vignettes en modifiant les lignes UPLOAD_FOLDER et HTML_PATH
par défaut : './static/uploads/'

Attention si le fichier n'est pas stocké dans static il faut modifier
la configuration du serveur flask sinon il va y avoir des problématiques
d'affichage de la vignette. (cf static folder flask)

###################  Fichier task_celery.py:  #########################
C'est le fichier de configuration de celery pour les taches asynchrone.

Il faut modifier la ligne UPLOAD_FOLDER en cas de changement de fichier
 d'enregistrement par défaut: './static/uploads/'

Il faut également modifier la ligne 4 en modifiant borker si l'adresse
 du serveur redis n'est pas: 'redis://guest@localhost:6379//'
################### Fichier test.py/Dossier image_test  ################

Fichier exécutable avec pytest et qui permet d'effectuer une suite de 
test vérifiant le bon fonctionnement du serveur

Fonctionne avec le dossier image_test qui contient une image (une image prise
avec mon téléphone pour avoir des métadonnées) et un fichier texte.

################### Dossier templates ###################################

Contiens les templates HTML pour l'affichage des pages web

################### Critiques et amélioration possibles #################

Les métadonnées ne sont pas au format JSON car il y a des problèmes avec 
certaines données qui sont au format bytes (mais pas tout) ce qui
nécessiterait la création d'une solution de tri.

Certaines erreurs pourraient être mieux indiquées (peut être avec le retour de
code d'erreurs)

Trouver une solution pour faire un fichier de configuration global pour ne
pas avoir à jongler entre les fichiers

Faire une base de données au lieu de fichier static

Rajouter des options comme une fonction de download du fichier, ect...

Mais bon si je me lance dans tout ça j'ai plus le temps pour le reste et 
comme ça fonctionne actuellement voilà!

Bon courage pour la correction!
(PS : Je conseille de jeter un oeil à l'image test ;) )

