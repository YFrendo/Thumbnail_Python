import unittest
import serveur_flask
import io
import os

class TestFlask(unittest.TestCase):

    def test_id_negatif(self):

        with serveur_flask.app.test_client() as c:
            reponse = c.get('/images/-1')
            reponse = reponse.data.decode('UTF-8')
            self.assertEqual(reponse, "Pas de photo à cette ID")

    def test_id_grand(self):

        with serveur_flask.app.test_client() as c:
            reponse = c.get('/images/10000000000')
            reponse = reponse.data.decode('UTF-8')
            self.assertEqual(reponse, "Pas de photo à cette ID")
     
    def test_faux(self):
        
        with serveur_flask.app.test_client() as c:
            reponse = c.get('/blabladodo')
            self.assertEqual(reponse.status_code, 404)

    def test_image(self):

        with serveur_flask.app.test_client() as c:

            with open('./image_test/Image_test.jpg', 'rb') as img:
                imgIO = io.BytesIO(img.read())
            data = {
                    'file' : (imgIO, 'Image_test.jpg')
                    }
            reponse = c.post('/images' , data=data, content_type = 'multipart/form-data')
            self.assertTrue(reponse.data.decode('UTF-8').isnumeric())

    def test_texte(self):

        with serveur_flask.app.test_client() as c:

            with open('./image_test/fichier_format_texte.txt', 'rb') as img:
                imgIO = io.BytesIO(img.read())
            data = {
                    'file' : (imgIO, 'Texte_test.txt')
                    }
            reponse = c.post('/images' , data=data, content_type = 'multipart/form-data')
            self.assertEqual(reponse.data.decode('UTF-8'),'Cannot open file')

    def test_crea_fichier(self):

        with serveur_flask.app.test_client() as c:

            with open('./image_test/Image_test.jpg', 'rb') as img:
                imgIO = io.BytesIO(img.read())
            data = {
                    'file' : (imgIO, 'Image_test.jpg')
                    }
            c.post('/images' , data=data, content_type = 'multipart/form-data')
            self.assertEqual(len(os.listdir('./static/uploads/0')),3)

    def test_affiche_vignette(self):

        with serveur_flask.app.test_client() as c:

            with open('./image_test/Image_test.jpg', 'rb') as img:
                imgIO = io.BytesIO(img.read())
            data = {
                    'file' : (imgIO, 'Image_test.jpg')
                    }
            c.post('/images' , data=data, content_type = 'multipart/form-data')
            reponse = c.get('/vignette/0')
            self.assertEqual(reponse.status_code, 200)

    def test_vignette_nonexistante(self):

        with serveur_flask.app.test_client() as c:

            with open('./image_test/Image_test.jpg', 'rb') as img:
                imgIO = io.BytesIO(img.read())
            data = {
                    'file' : (imgIO, 'Image_test.jpg')
                    }
            c.post('/images' , data=data, content_type = 'multipart/form-data')
            reponse = c.get('/vignette/10000')
            self.assertEqual(reponse.data.decode("UTF-8"),'Pas de vignette')
