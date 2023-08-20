
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

