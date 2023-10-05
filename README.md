
# auth-reg backend (REST API)

A simple Authentication & Registration backend API built with the Django REST framework. It is intended to be used by frontend clients (React, Vue, etc).


### API Reference

#### 1. User Login

Endpoint security: protected

```http
POST /login
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. User username |
| `password` | `string` | **Required**. User password |

#### 2. User Registration

Endpoint security: open

```http
POST /register
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `first_name`      | `string` | **Required**. First name of user |
| `last_name`      | `string` | **Required**. Last name of user |
| `email`      | `string` | **Required**. User email|
| `username`      | `string` | **Required**. User username |
| `password`      | `string` | **Required**. User password |

#### 3. User Profile

Endpoint security: protected

```http
GET /profile
```

#### 4. User Account Activation

Endpoint security: open

```http
GET /activate-account/?token=[token]
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `token`      | `string` | **Required**. activation token, received from /register |

#### 5. Change Password 

Endpoint security: protected

```http
POST /change-password
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `current_password`      | `string` | **Required**. current password of user |
| `current_password`      | `string` | **Required**. new password |



### Local Setup 

clone repository.

```bash
  git clone https://github.com/codeSolomons/auth-reg-backend.git
```

create .env file in /core directory and insert the following env vars.

`SECRET_KEY={random string}` 

`DEBUG=True`

`ALLOWED_HOSTS=localhost,127.0.0.1`

`ENV=development`

create virtual environment, activate it (commands used on a windows machine, if it does not work for you, google how to do the same thing on a different OS).

```bash
  python -m venv venv
```
```bash
  venv\Scripts\activate
```

Install project requirements.

```bash
  pip install -r requirements.txt
```

Run dev server.

```bash
  python manage.py runserver
```

