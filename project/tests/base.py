from flask_testing import TestCase
from run_tests import app, db

class BaseTestCase(TestCase):
    def create_app(self):
        self.app = app
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
