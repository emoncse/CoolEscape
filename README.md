
# CoolEscape

CoolEscape is a Django-based web application that helps users:  

1. **Find the Coolest Districts** – Identify the districts in Bangladesh with the lowest temperatures.  
2. **Compare Weather for Travel** – Check the weather of two locations on a specific date and determine if travel is suitable.  
3. **Secure Access** – Uses JWT authentication for secure user access.  
4. **API Documentation** – Built with Django Rest Framework (DRF) and drf-spectacular for API schema generation and documentation.  

## Table of Contents

- Installation
- Setup
- API Endpoints
- Swagger API Documentation
- Using Postman

## Installation

### Prerequisites

- Python 3.12.8
- Django 5.1.6
- Virtualenv

### Steps

1. Clone the repository:

```
git clone https://github.com/emoncse/CoolEscape.git
cd CoolEscape
```

2. Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

4. Apply the migrations:

```
python manage.py makemigrations
python manage.py migrate
```

5. Collect static files:

```
python manage.py collectstatic
```

6. Create a superuser:

```
python manage.py createsuperuser
```

7. Run the development server:

```
python manage.py runserver
```

8. Open the server link:

```
https://127.0.0.1:8000
```


## Docker Installation

### Prerequisites
1. Docker
2. Docker Compose
3. Git

### Steps
1. Clone the repository:
```sh 
git clone `https://github.com/emoncse/CoolEscape.git`
````

2. Change directory to the project folder:
```sh
cd CoolEscape
```

3. Build the Docker image and Run the Docker container:
```sh
docker compose up --build
```

4. Run the Docker container in the background:
```sh
docker compose up -d
```


## Setup

## API Endpoints

### Authentication

- Obtain Token: `POST /api/token/`
- Refresh Token: `POST /api/token/refresh/`

### Coolest Districts API

- Get the coolest districts: `GET /v1/coolest-districts/`

### Travel Advice API

- Get Travel Advice: `GET /v1/travel-destination/`

[//]: # (### User Management API)

[//]: # (- Get All Users: `GET /API/users/`)

[//]: # (- Create User: `POST /API/users/`)

[//]: # (- Get User by Username: `GET /API/users/{username}/`)

[//]: # (- Update User by Username: `PUT /API/users/{username}/`)

[//]: # (      - must send authorization token in request body)

[//]: # (- Partially Update User by Username: `PATCH /API/users/{username}/`)

[//]: # (      - must send authorization token in request body)

[//]: # (- Delete User by Username: `DELETE /API/users/{username}/`)

[//]: # (        - must send authorization token in request body)

[//]: # (- Get All Log: `GET /API/logs/`)

[//]: # (- Get Log by id: `GET /API/logs/{id}`)

## Swagger API Documentation

- CoolEscape API Documentation
- Version: 1.0.0
- OAS: 3.0

### Swagger URL

- **Swagger**: `http://127.0.0.1:8000/api/docs/`
- **Cool Escape API Documentation**

[//]: # (### User Management)

[//]: # ()
[//]: # (- **GET** `/API/users/`)

[//]: # (- **POST** `/API/users/`)

[//]: # (- **GET** `/API/users/{username}/`)

[//]: # (- **PUT** `/API/users/{username}/`)

[//]: # (- **PATCH** `/API/users/{username}/`)

[//]: # (- **DELETE** `/API/users/{username}/`)

### API

- **POST** `/api/token/`
- **POST** `/api/token/refresh/`

## Using Postman

### Obtain Token

1. **URL**: `http://127.0.0.1:8000/api/token/`
2. **Method**: `POST`
3. **Body**: 
   ```
   {
       "username": "your_username",
       "password": "your_password"
   }
   ```

### Access Protected Endpoints

1. **URL**: `http://127.0.0.1:8000/v1/*/`
2. **Method**: `GET`
3. **Headers**:
   - Key: `Authorization`
   - Value: `Bearer <access_token>`

Replace `<access_token>` with the token obtained in the previous step.

### Refresh Token

1. **URL**: `http://127.0.0.1:8000/api/token/refresh/`
2. **Method**: `POST`
3. **Body**:
   ```
   {
       "refresh": "<refresh_token>"
   }
   ```

