import unittest
import serveur_flask
import io

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

    def test_texte(self):

        with serveur_flask.app.test_client() as c:

            with open('./image_test/Image_test.jpg', 'rb') as img:
                imgIO = io.BytesIO(img.read())
            data = {
                    'file' : (imgIO, 'Image_test.jpg')
                    }
            reponse = c.post('/images' , data=data, content_type = 'multipart/form-data')
            print(reponse.data)
            self.assertTrue(reponse.data.decode('UTF-8').isnumeric())

