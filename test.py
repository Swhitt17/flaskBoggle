from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

 def setUp(self):
  self.client = app.test_client()
  app.config['TESTING']= True


 def test_homepage(self):
  with app.test_client() as client:
   res = client.get('/')
   self.assertIn("board",session)
   self.assertIsNone(session.get("highscore"))
   self.assertIsNone(session.get("nplays"))
   self.assertIn("b'<p>High Score:",res.data)
   self.assertIn("b'Score",res.data)
   self.assertIn("b' Seconds left:",res.data)

 def test_valid_word(self):
  with app.test_client() as client:
   with client.seesion_transaction() as sess:
    sess["board"] = [["B", "U", "G", "G", "G"],
                     ["B", "U", "G", "G", "G"],
                     ["B", "U", "G", "G", "G"],
                     ["B", "U", "G", "G", "G"],
                     ["B", "U", "G", "G", "G"]]
   res = client.get('/check-guess?word=bug')
  self.assertEqual(res.json['result'], "ok")

 def test_invaild_word(self):
   with app.test_client() as client:
    res = client.get('/check-guess?word=banana')
    self.assertEqual(res.json['result'], "not-on-board")

 def non_english_word(self):
  with app.test_client() as client:
   res = client.get('/check-guess?word=fiujkushnfs')
  self.assertEqual(res.json['result'], "not-word")