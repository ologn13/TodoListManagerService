import unittest
from project import create_app, db
from flask_jwt_extended import JWTManager
from flask_restful import Api
from project.manage_resources import ResourcesManager

app = create_app()
jwt = JWTManager(app)
ResourcesManager.add_resources(app)

from project import schema

@app.before_first_request
def create_tables():
    db.create_all()

@jwt.token_in_blacklist_loader
def token_blacklisting_check(raw_token):
    """"
    Called before every request if the endpoint is jwt (whether refresh or access) protected
    """
    token = raw_token['jti']
    return schema.RevokedTokens.is_token_revoked(token)

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')