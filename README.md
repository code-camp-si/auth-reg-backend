
# auth-reg backend (REST API)

A simple Authentication & Registration backend API built with the Django REST framework. It is intended to be used by frontend clients (React, Vue, etc).


### API Reference

#### User Login

```http
POST /login
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. User username |
| `password` | `string` | **Required**. User password |

#### User Registration

```http
POST /register
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `full_name`      | `string` | **Required**. Full name of user |
| `email`      | `string` | **Required**. User email|
| `username`      | `string` | **Required**. User username |
| `password`      | `string` | **Required**. User password |




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

