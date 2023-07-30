import unittest
from flask import json
from ..app import create_app
from ..db import db
from ..models.user import UserModel


class UserTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None