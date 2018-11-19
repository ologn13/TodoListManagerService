# TodoListManagerService
REST APIs for doing CRUD operations on tasks specific for each user

## Pre-requisites
docker, docker-compose must be setup

POSTMAN can be used to make requests to api's.

## How to run server and tests?
cd TodoListManagerService

docker-compose -f docker-compose-dev.yml up --build

docker-compose -f docker-compose-dev.yml run todolistmanagerservice python run_tests.py test

Server will be up and running at http://localhost:5000/

## User Registration API Info

### Register User: POST /user/register

Request body:

    {
        "username": "vikrant",
        "password": "vikrant123"
        "email": "vikrantiitr1@gmail.com"
    }

Response body:
    
    {
        'message': 'User vikrant was created',
        'access_token': access_token,
         'refresh_token': refresh_token
     }

### Login User: POST /user/login

Request body:

    {
        "username": "vikrant",
        "password": "vikrant123"
    }

Response body:
    
    {
        'message': 'User vikrant is logged in.',
        'access_token': access_token,
         'refresh_token': refresh_token
     }

### Update User: POST /user/update

Request Header:

    {
        "Authorization": "Bearer [access_token]",
    }

Request body:

    {
        'email': "vikrantiitr2@gmail.com"
    }

Response body:
    
    {
        'message': 'User vikrant data successfully updated',
     }

### Revoke Access Token(Logout): POST /user/access/logout

Request Header:

    {
        "Authorization": "Bearer [access_token]",
    }

Response body:
    
    {
        'message': 'Successfully revoked access token',
     }

### Revoke Refresh Token(Logout): POST /user/refresh/logout

Request Header:

    {
        "Authorization": "Bearer [refresh_token]",
    }

Response body:
    
    {
        'message': 'Successfully revoked refresh token',
     }

### Refresh Token: POST /user/token/refresh

Request Header:

    {
        "Authorization": "Bearer [refresh_token]",
    }

Response body:
    
    {
        'access_token': access_token,
     }

## Task Management API Info

### Create Task: POST /tasks/create

Request Header:

    {
        "Authorization": "Bearer [access_token]",
    }

Request body:

    {
        'heading': "Task1",
        'description': "Task1 description"
    }

Response body:
    
    {
        'message': 'Task was created successfully',
        'id': task id
     }
     
### Get Task: GET /tasks/[id]

Request Header:

    {
        "Authorization": "Bearer [access_token]",
    }

Response body:
    
    {
         'id': task id,
         'heading': task heading,
         'description': task description,
         'is_completed': str(task is_completed)
    }

### List Tasks: GET /tasks

Request Header:

    {
        "Authorization": "Bearer [access_token]",
    }

Response body: List of tasks
    
    [{
         'id': task id,
         'heading': task heading,
         'description': task description,
         'is_completed': str(task is_completed)
    }]

### Update Task: POST /tasks/[id]/update

Request Header:

    {
        "Authorization": "Bearer [access_token]",
    }

Request body:

    {
        "heading": new heading if any,
        "description": new description if any,
        "is_completed": "True" or "False"
    }

Response body: Updated task attributes
    
    {
         'message': 'Task updated successfully',
         'id': task id,
         'heading': task heading,
         'description': task description,
         'is_completed': str(task is_completed)
    }

### Delete Task: POST /tasks/[id]/delete

Request Header:

    {
        "Authorization": "Bearer [access_token]",
    }

Response body:
    
    {
         'message': 'Task Deleted Successfully'
    }

