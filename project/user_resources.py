from flask_restful import Resource, abort
from project.parsers import Parser
from project.schema import User, RevokedTokens
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)


class RegisterUser(Resource):
    """"
    Registers a new User into the system
    """
    def post(self):
        user_parser = Parser.get_user_parser(password_req=True, email_req=True)
        user_data = user_parser.parse_args()
        if User.get_user_by_name(user_data['username']) or User.get_user_by_email(user_data['email']):
            abort(409, description="User with username - %s  or email %s is already present" % (
                user_data['username'], user_data['email']))

        user = User(
            username=user_data['username'],
            password=User.generate_hash(user_data['password']),
            email=user_data['email']
        )

        try:
            user.save()
            access_token = create_access_token(identity=user_data['username'])
            refresh_token = create_refresh_token(identity=user_data['username'])
            return {
                'message': 'User {} was created'.format(user_data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except:
            abort(500, description="User creation failed")


class UpdateUser(Resource):
    """"
    Updates user information.
    Endpoint is jwt protected
    """
    @jwt_required
    def post(self):

        def has_valid_email(user_data):
            if 'email' not in user_data:
                return False
            email = user_data['email']
            if email == None or len(email) == 0:
                return False
            return True

        user_parser = Parser.get_user_parser(username_req=False)
        user_data = user_parser.parse_args()
        username = get_jwt_identity()
        user = User.get_user_by_name(username=username)
        email = user.email if (not has_valid_email(user_data)) else user_data['email']
        try:
            User.update_user(username=username, email=email)
            return {'message': 'User %s data successfully updated' % username}
        except:
            abort(500, description="Failed to update user %s data" % username)


class LoginUser(Resource):
    """"
    Handles a user login request
    """
    def post(self):
        user_parser = Parser.get_user_parser(username_req=True, password_req=True)
        user_data = user_parser.parse_args()
        user = User.get_user_by_name(user_data['username'])

        if not user:
            abort(400, description="Username %s doesn't exist" % user_data['username'])

        if User.verify_hash(user_data['password'], user.password):
            access_token = create_access_token(identity=user_data['username'])
            refresh_token = create_refresh_token(identity=user_data['username'])
            return {
                'message': 'User {} is logged in.'.format(user_data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            abort(401, description="Password is not correct")


class LogoutUserAccess(Resource):
    """"
    Handles user's logout request
    Protecting the endpoint with a valid access token using jwt_required decorator
    """
    @jwt_required
    def post(self):
        token = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokens(token=token)
            revoked_token.save()
            return {'message': 'Successfully revoked access token'}
        except:
            abort(500, description='failed to revoke access token')


class LogoutUserRefresh(Resource):
    """"
    Handles user's logout request
    Protecting the endpoint with a valid refresh token using jwt_refresh_token_required
    """
    @jwt_refresh_token_required
    def post(self):
        token = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokens(token=token)
            revoked_token.save()
            return {'message': 'Successfully revoked refresh token'}
        except:
            abort(500, description='failed to revoke refresh token')


class RefreshToken(Resource):
    """"
    Allows user to refresh token.
    Endpoint is protected with jwt_refresh_token_required
    """
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {"access_token": access_token}
