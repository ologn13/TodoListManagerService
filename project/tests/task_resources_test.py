import json
import unittest
from project.tests.base import BaseTestCase


class TaskTestUtil():
    """
    Utility data members and methods for use in TaskResources tests.
    """
    user_data = {
        'username': 'vikrant', 'password': 'vikrant462', 'email': 'vikrantiitr1@gmail.com'
    }
    task_valid_data_1 = {
        'heading':'Task1', 'description':'Task1 Description'
    }
    task_valid_data_2 = {
        'heading': 'Task2', 'description': 'Task2 Description'
    }
    task_invalid_data = {'heading': 'Task1'}
    task_update_valid_data = {'is_completed': 'True'}

    @staticmethod
    def get_access_token(client):
        """
        Given the flask app client, it returns an access token for the valid user data
        :param client:
        :return: access_token
        """
        client.post('/user/register', data=TaskTestUtil.user_data)
        response = client.post('/user/login', data=TaskTestUtil.user_data)
        data = json.loads(response.data.decode())
        return data["access_token"]

    @staticmethod
    def create_two_tasks(client):
        """
        Given the flask app client, it creates two tasks with valid data
        :param client:
        :return: id of task1, id of task2, access_token
        """
        access_token = TaskTestUtil.get_access_token(client)
        response1 = client.post('/tasks/create', headers=dict(Authorization="Bearer " + access_token),
                    data=TaskTestUtil.task_valid_data_1)
        data1 = json.loads(response1.data.decode())
        response2 = client.post('/tasks/create', headers=dict(Authorization="Bearer " + access_token),
                    data=TaskTestUtil.task_valid_data_2)
        data2 = json.loads(response2.data.decode())
        return data1['id'], data2['id'], access_token


class TestTaskResources(BaseTestCase, TaskTestUtil):

    def test_create_valid_data(self):
        """
        Tests if a tasks can be created with valid data
        """
        access_token = TaskTestUtil.get_access_token(self.client)
        response = self.client.post('/tasks/create', headers=dict(Authorization="Bearer " + access_token),
                                    data=TaskTestUtil.task_valid_data_1)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id' in data and data['id'] == 1)

    def test_create_invalid_data(self):
        """
        Tests if the task is not allowed to be created with invalid data (missing description)
        """
        access_token = TaskTestUtil.get_access_token(self.client)
        response = self.client.post('/tasks/create', headers=dict(Authorization="Bearer " + access_token),
                                    data=TaskTestUtil.task_invalid_data)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertTrue('message' in data and 'description' in data['message'])  # description missing param

    def test_get_valid_data(self):
        """
        Tests if a task with valid task id can be retrieved successfully.
        """
        id1, id2, access_token = TaskTestUtil.create_two_tasks(self.client)
        response1 = self.client.get('/tasks/%d' % id1, headers=dict(Authorization="Bearer " + access_token))
        data1 = json.loads(response1.data.decode())
        response2 = self.client.get('/tasks/%d' % id2, headers=dict(Authorization="Bearer " + access_token))
        data2 = json.loads(response2.data.decode())
        self.assertEquals(response1.status_code, 200)
        self.assertEquals(response2.status_code, 200)
        self.assertTrue('id' in data1 and data1['id'] == id1)
        self.assertTrue('is_completed' in data1 and data1['is_completed'] == "False")
        self.assertTrue('heading' in data1 and 'description' in data1)
        self.assertTrue('id' in data2 and data2['id'] == id2)
        self.assertTrue('is_completed' in data2 and data2['is_completed'] == "False")
        self.assertTrue('heading' in data2 and 'description' in data2)

    def test_get_invalid_data(self):
        """
        Tests if the GetTask api handles invalid data well.
        """
        id1, id2, access_token = TaskTestUtil.create_two_tasks(self.client)
        response = self.client.get('/tasks/%d' % (id2+1), headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 409)

    def test_list(self):
        """
        Tests if all the tasks associated with the user (logged in) can be retrieved successfully.
        """
        id1, id2, access_token = TaskTestUtil.create_two_tasks(self.client)
        response = self.client.get('/tasks', headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        res_ids = (data[0]['id'], data[1]['id'])
        self.assertTrue(id1 in res_ids and id2 in res_ids)

    def test_list_empty(self):
        """
        Tests if the ListTasks api handles the request well for zero tasks
        """
        access_token = TaskTestUtil.get_access_token(self.client)
        response = self.client.get('/tasks', headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 0)

    def test_update(self):
        """
        Tests if a task can be successfully updated.
        """
        id1, id2, access_token = TaskTestUtil.create_two_tasks(self.client)
        response = self.client.post('/tasks/%d/update' %id1, headers=dict(Authorization="Bearer " + access_token),
                                    data=TaskTestUtil.task_update_valid_data)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id' in data and data['id'] == id1)
        self.assertTrue('is_completed' in data and data['is_completed'] == 'True')

    def test_delete_valid_data(self):
        """
        Tests if a valid task can be successfully deleted
        """
        id1, id2, access_token = TaskTestUtil.create_two_tasks(self.client)
        response = self.client.post('/tasks/%d/delete' % id1, headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in data and "Success" in data['message'])

    def test_delete_invalid_data(self):
        """
        Tests if the DeleteTask api handles well the request for task not present in the system
        """
        id1, id2, access_token = TaskTestUtil.create_two_tasks(self.client)
        response = self.client.post('/tasks/%d/delete' % (id2+1), headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 409)
