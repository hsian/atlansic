import unittest
import json
import re
from base64 import b64encode
from flask import g
from app import create_app, db
from app.models import Captcha, Role, User

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

    def test_captcha(self):
        res = self.client.post(
            '/api/captcha/',
            data = json.dumps({ 'mobile': '1234' }),
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )
        # 退出测试环境修改验证码valid的线程。
        g.t.cancel()
        self.assertEqual(res.status_code, 200)

    def test_register(self):
        self.test_captcha()
        res = self.client.post(
            '/api/register/',
            data = json.dumps({
                'username': '1234',
                'password': '123',
                'captcha': '2233'
            }),
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_login(self):
        pass