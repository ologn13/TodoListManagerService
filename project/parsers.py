from flask_restful import reqparse

class Parser:
    """"
    Returns Parsers for REST Requests
    """
    @staticmethod
    def get_user_parser(id_req=False, username_req=True, password_req=False, email_req=False):
        user_parser = reqparse.RequestParser()
        user_parser.add_argument('id', required=id_req)
        user_parser.add_argument('username', required=username_req)
        user_parser.add_argument('password', required=password_req)
        user_parser.add_argument('email', required=email_req)
        return user_parser

    @staticmethod
    def get_tasks_parser(id_req=True, heading_req=False, desc_req=False, status_req=False):
        task_parser = reqparse.RequestParser()
        task_parser.add_argument('id', required=id_req)
        task_parser.add_argument('heading', required=heading_req)
        task_parser.add_argument('description', required=desc_req)
        task_parser.add_argument('is_completed', required=status_req)
        return task_parser
