# API Documentation

First `make up` the project then visit the URL: `http://localhost/api/`

Currently we have to main api entries (endpoints).

-   Patients: `/api/patients/`
-   Studies of patient: `/api/patients/{patient_id}/studies/`

## Patients

| Method | URL                | Description                   |
| ------ | ------------------ | ----------------------------- |
| GET    | `/api/patients/`   | Get list of patients          |
| GET    | `/api/patients/1/` | Get patient detail            |
| POST   | `/api/patients/1/` | Create a new patient          |
| PUT    | `/api/patients/1/` | Update all fields of patient  |
| PATCH  | `/api/patients/1/` | Update partial fields patient |
| DELETE | `/api/patients/1/` | Delete a patient              |

### `GET /api/patients/`

Query parameters:

| Parameter   | Type  | Description                                                      | Default |
| ----------- | ----- | ---------------------------------------------------------------- | ------- |
| only-active | `int` | If set `1` only show the active patients, else show all patients | `1`     |

Response Example:

```json
[
    {
        "id": 1,
        "first_name": "Luis",
        "last_name": "Hernandez",
        "birth_date": null,
        "email": "luis@gmail.com",
        "is_active": true
    }
]
```

### `GET /api/patients/1/`

Response Example:

```json
{
    "id": 1,
    "first_name": "Luis",
    "last_name": "Hernandez",
    "birth_date": null,
    "email": "luis@gmail.com",
    "is_active": true
}
```

### `POST /api/patients/`, `PUT /api/patients/1/`

Body parameters (json/form-data):

| Parameter  | Type   | Optional | Description                              |
| ---------- | ------ | -------- | ---------------------------------------- |
| first_name | `str`  | No       | Patient first name                       |
| last_name  | `str`  | No       | Patient last name                        |
| birth_date | `str`  | No       | Patient birth date format (`YYYY-MM-DD`) |
| email      | `str`  | No       | Patient email                            |
| is_active  | `bool` | No       | Patient logical erase                    |

Request Example:

```json
{
    "first_name": "Hugo",
    "last_name": "Sandoval",
    "birth_date": "1995-12-13",
    "email": "hhsm@gmail.com",
    "is_active": true
}
```

Response Example:

```json
{
    "id": 1
}
```

### `PATCH /api/patients/1/`

Body parameters (json/form-data):

| Parameter  | Type   | Optional | Description                              |
| ---------- | ------ | -------- | ---------------------------------------- |
| first_name | `str`  | Yes      | Patient first name                       |
| last_name  | `str`  | Yes      | Patient last name                        |
| birth_date | `str`  | Yes      | Patient birth date format (`YYYY-MM-DD`) |
| email      | `str`  | Yes      | Patient email                            |
| is_active  | `bool` | Yes      | Patient logical erase                    |

Request Example:

```json
{
    "first_name": "Héctor Hugo"
}
```

Response Example:

```json
{
    "id": 1
}
```

### `DELETE /api/patients/1/`

Response Example:

```json
{
    "id": 1
}
```

## Studies of patient

| Method | URL                          | Description                            |
| ------ | ---------------------------- | -------------------------------------- |
| GET    | `/api/patients/1/studies/`   | Get list of studies of patient         |
| GET    | `/api/patients/1/studies/1/` | Get study detail of patient            |
| POST   | `/api/patients/1/studies/1/` | Create a new study of patient          |
| PUT    | `/api/patients/1/studies/1/` | Update all fields of study of patient  |
| PATCH  | `/api/patients/1/studies/1/` | Update partial fields study of patient |
| DELETE | `/api/patients/1/studies/1/` | Delete a study of patient              |

### `GET /api/patients/1/studies/`

Query parameters:

| Parameter   | Type  | Description                                                      | Default |
| ----------- | ----- | ---------------------------------------------------------------- | ------- |
| only-active | `int` | If set `1` only show the active patients, else show all patients | `1`     |

Response Example:

```json
[
    {
        "id": 1,
        "urgency_level": "LOW",
        "body_part": "ARM",
        "description": "LEFT",
        "type": "XRAY",
        "is_active": true
    }
]
```

### `GET /api/patients/1/studies/1/`

Response Example:

```json
{
    "id": 1,
    "urgency_level": "LOW",
    "body_part": "ARM",
    "description": "LEFT",
    "type": "XRAY",
    "is_active": true
}
```

### `POST /api/patients/1/studies/1/`, `PUT /api/patients/1/studies/1/`

Body parameters (json/form-data):

| Parameter     | Type   | Optional | Description                    |
| ------------- | ------ | -------- | ------------------------------ |
| urgency_level | `str`  | No       | Study urgency (LOW, MID, HIGH) |
| body_part     | `str`  | No       | Study body part                |
| description   | `str`  | No       | Study description              |
| type          | `str`  | No       | Study type (XRAY, MAMMOGRAM)   |
| is_active     | `bool` | No       | Study logical erase            |

Request Example:

```json
{
    "urgency_level": "LOW",
    "body_part": "ARM",
    "description": "LEFT",
    "type": "XRAY",
    "is_active": true
}
```

Response Example:

```json
{
    "id": 1
}
```

### `PATCH /api/patients/1/studies/1/`

Body parameters (json/form-data):

| Parameter     | Type   | Optional | Description                    |
| ------------- | ------ | -------- | ------------------------------ |
| urgency_level | `str`  | Yes      | Study urgency (LOW, MID, HIGH) |
| body_part     | `str`  | Yes      | Study body part                |
| description   | `str`  | Yes      | Study description              |
| type          | `str`  | Yes      | Study type (XRAY, MAMMOGRAM)   |
| is_active     | `bool` | Yes      | Study logical erase            |

Request Example:

```json
{
    "urgency_level": "LOW"
}
```

Response Example:

```json
{
    "id": 1
}
```

### `DELETE /api/patients/1/studies/1/`

Response Example:

```json
{
    "id": 1
}
```
