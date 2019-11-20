import unittest
import json
import re
from base64 import b64encode
from flask import g
from app import create_app, db
from app.user.model import Captcha, Role, User

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app  = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_roles(self):
        res = self.client.get(
            '/api/user/roles/'
        )
        self.assertEqual(res.status_code, 200)

   