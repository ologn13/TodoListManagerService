import json
import unittest
from project.tests.base import BaseTestCase


class UserTestUtil():
    """
    Utility data members and methods for use in UserResources tests.
    """
    user_register_valid_data = {
        'username': 'vikrant', 'password': 'vikrant462', 'email': 'vikrantiitr1@gmail.com'
    }
    user_register_invalid_data = {'username':'vikrant', 'email':'vikrantiitr1@gmail.com'}
    user_login_valid_data = {'username': 'vikrant', 'password': 'vikrant462'}
    user_login_invalid_data = {'username': 'vikrant', 'password': 'null'}
    user_update_data = {'email': 'vikrantiitr2@gmail.com'}

    @staticmethod
    def register_user(client):
        """
        Given the flask app client, it registers a user with valid user data.
        :param client:
        :return: response, data
        """
        response = client.post('/user/register', data=UserTestUtil.user_register_valid_data)
        data = json.loads(response.data.decode())
        return response, data

    @staticmethod
    def login_user(client):
        """
        Given the flask app client, it logs in the user with the valid data.
        :param client:
        :return: response, data
        """
        response = client.post('/user/login', data=UserTestUtil.user_login_valid_data)
        data = json.loads(response.data.decode())
        return response, data


class TestUserResources(BaseTestCase, UserTestUtil):
    """Tests for the User Resources"""

    def test_register_valid_data(self):
        """
        Tests if a user can be successfully registered with given data and
        disallows duplicate data.
        """
        response1 = self.client.post('/user/register', data=UserTestUtil.user_register_valid_data)
        data1 = json.loads(response1.data.decode())

        # duplicate data request
        response2 = self.client.post('/user/register', data=UserTestUtil.user_register_valid_data)
        self.assertEqual(response1.status_code, 200)
        self.assertTrue("access_token" in data1)
        self.assertTrue("refresh_token" in data1)
        self.assertEqual(response2.status_code, 409)

    def test_register_invalid_data(self):
        """
        Tests if a user is not allowed to be registered for invalid data.
        """
        response = self.client.post('/user/register', data=UserTestUtil.user_register_invalid_data)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertTrue('message' in data)
        self.assertTrue('password' in data['message'])  # the missing parameter

    def test_login_valid(self):
        """"
        Tests if a valid user can be logged in.
        """
        UserTestUtil.register_user(self.client)
        response = self.client.post('/user/login', data=UserTestUtil.user_login_valid_data)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue("access_token" in data)
        self.assertTrue("refresh_token" in data)

    def test_login_invalid(self):
        """"
        Tests if an invalid user is disallowed.
        """
        UserTestUtil.register_user(self.client)
        response = self.client.post('/user/login', data=UserTestUtil.user_login_invalid_data)
        self.assertEqual(response.status_code, 401)

    def test_update(self):
        """"
        Tests if a user's data can be updated successfully
        """
        UserTestUtil.register_user(self.client)
        _, data = UserTestUtil.login_user(self.client)
        access_token = data["access_token"]
        response = self.client.post('/user/update', headers=dict(Authorization="Bearer " + access_token),
                                    data=UserTestUtil.user_update_data)
        self.assertEqual(response.status_code, 200)

    def test_logout_access(self):
        """
        Tests if a user's access token can be successfully revoked or not
        """
        UserTestUtil.register_user(self.client)
        _, data = UserTestUtil.login_user(self.client)
        access_token = data["access_token"]
        response = self.client.post('/user/access/logout', headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Success" in data['message'])


    def test_logout_refresh(self):
        """
        Tests if a user's refresh token can be successfully revoked or not
        """
        UserTestUtil.register_user(self.client)
        _, data = UserTestUtil.login_user(self.client)
        refresh_token = data["refresh_token"]
        response = self.client.post('/user/refresh/logout', headers=dict(Authorization="Bearer " + refresh_token))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Success" in data['message'])

    def test_refresh_token(self):
        """
        Tests if an access token can be generated using the refresh token or not
        """
        UserTestUtil.register_user(self.client)
        _, data = UserTestUtil.login_user(self.client)
        refresh_token = data["refresh_token"]
        response = self.client.post('/user/token/refresh', headers=dict(Authorization="Bearer " + refresh_token))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue("access_token" in data)


if __name__ == '__main__':
    unittest.main()