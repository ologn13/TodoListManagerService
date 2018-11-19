from flask_restful import Resource, abort
from flask import jsonify
from project.parsers import Parser
from project.schema import User, Task
import sqlalchemy
from flask_jwt_extended import (jwt_required, get_jwt_identity)


class CreateTask(Resource):
    """
    Given a request with params {"heading", "description"}
    Endpoint is jwt protected
    """

    @jwt_required
    def post(self):
        task_parser = Parser.get_tasks_parser(id_req=False, heading_req=True, desc_req=True)
        task_data = task_parser.parse_args()
        username = get_jwt_identity()
        user = User.get_user_by_name(username=username)

        task = Task(
            user_id=user.id,
            heading=task_data['heading'],
            description=task_data['description'],
            is_completed=False
        )
        try:
            task.save()
            return {
                'message': 'Task was created successfully',
                'id': task.id
            }
        except:
            abort(500, description="Failed to create task")


class GetTask(Resource):
    """
    Retrieve a task given "id" of task in params
    Endpoint is jwt protected
    """

    @jwt_required
    def get(self, id):
        try:
            task = Task.get_task_by_id(id)
            if task == None:
                raise KeyError
            return {
                'id': task.id,
                'heading': task.heading,
                'description': task.description,
                'is_completed': str(task.is_completed)
            }
        except KeyError:
            abort(409, description='Task %d does not exist' % id)
        except:
            abort(500, description="Unknown exception occured")


class ListTasks(Resource):
    """
    Lists all the tasks for the user logged in.
    Endpoint is jwt protected
    """

    @jwt_required
    def get(self):
        username = get_jwt_identity()
        user = User.get_user_by_name(username=username)
        tasks = user.tasks
        list_of_tasks = []
        for task in tasks:
            list_of_tasks.append({
                'id': task.id,
                'heading': task.heading,
                'description': task.description,
                'is_completed': str(task.is_completed)
            })
        return jsonify(list_of_tasks)


class UpdateTask(Resource):
    """
    Updates a given task. Params may include any of {"heading", "description", "is_completed"}
    Endpoint is jwt protected
    """

    @jwt_required
    def post(self, id):
        task_parser = Parser.get_tasks_parser(id_req=False)
        task_data = task_parser.parse_args()
        task = Task.get_task_by_id(id=id)
        heading = task.heading if ('heading' not in task_data or task_data['heading'] == None) else task_data[
            'heading']
        description = task.description if ('description' not in task_data or task_data['description'] == None) else \
        task_data['description']
        is_completed = task.is_completed if (
                    'is_completed' not in task_data or task_data['is_completed'] == None) else task_data[
            'is_completed']

        try:
            Task.update_task(id=id, heading=heading, description=description, is_completed=bool(is_completed))
            return {
                'message': 'Task updated successfully',
                'id': id,
                'heading': heading,
                'description': description,
                'is_completed': is_completed
            }
        except:
            abort(500, description="Failed to updated task %d" % id)


class DeleteTask(Resource):
    """
    Deletes a task given the task id
    Endpoint is jwt protected
    """

    @jwt_required
    def post(self, id):
        try:
            Task.delete_task(id=id)
            return {
                'message': 'Task Deleted Successfully'
            }
        except sqlalchemy.orm.exc.UnmappedInstanceError:
            abort(409, description="Task %d does not exist" % id)
        except:
            abort(500, description="Failed to delete task %d" % id)
