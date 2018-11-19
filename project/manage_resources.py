from flask_restful import Api
from project import user_resources, task_resources


class ResourcesManager():

    @staticmethod
    def add_resources(app=None):
        api = Api(app)
        api.add_resource(user_resources.RegisterUser, '/user/register')
        api.add_resource(user_resources.UpdateUser, '/user/update')
        api.add_resource(user_resources.LoginUser, '/user/login')
        api.add_resource(user_resources.LogoutUserAccess, '/user/access/logout')
        api.add_resource(user_resources.LogoutUserRefresh, '/user/refresh/logout')
        api.add_resource(user_resources.RefreshToken, '/user/token/refresh')

        api.add_resource(task_resources.CreateTask, '/tasks/create')
        api.add_resource(task_resources.GetTask, '/tasks/<int:id>')
        api.add_resource(task_resources.ListTasks, '/tasks')
        api.add_resource(task_resources.UpdateTask, '/tasks/<int:id>/update')
        api.add_resource(task_resources.DeleteTask, '/tasks/<int:id>/delete')