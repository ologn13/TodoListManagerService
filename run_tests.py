from project import create_app, db
from flask.cli import FlaskGroup
from flask_jwt_extended import JWTManager
from project.manage_resources import ResourcesManager
import unittest

app = create_app('project.config.TestingConfig')
jwt = JWTManager(app)
cli = FlaskGroup(app)
ResourcesManager.add_resources(app)

from project import schema

@jwt.token_in_blacklist_loader
def token_blacklisting_check(raw_token):
    """"
    Called before every request if the endpoint is jwt (whether refresh or access) protected
    """
    token = raw_token['jti']
    return schema.RevokedTokens.is_token_revoked(token)

@cli.command()
def test():
    """ Runs the unit tests"""
    tests = unittest.TestLoader().discover('project/tests', pattern='*_test.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__=="__main__":
    cli()