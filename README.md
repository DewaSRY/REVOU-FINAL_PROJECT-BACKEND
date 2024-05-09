[![Build Status](https://travis-ci.org/ssfdust/full-stack-flask-smorest.svg?branch=master)](https://travis-ci.org/ssfdust/full-stack-flask-smorest)
[![Coverage Status](https://s3.amazonaws.com/assets.coveralls.io/badges/coveralls_81.svg)](https://coveralls.io/github/ssfdust/full-stack-flask-smorest?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/aa3d7d986faf4e22969c56be5ea3d54d)](https://www.codacy.com/manual/ssfdust/full-stack-flask-smorest?utm_source=github.com&utm_medium=referral&utm_content=ssfdust/full-stack-flask-smorest&utm_campaign=Badge_Grade)
[![Python Versions](https://img.shields.io/badge/python-3.11%20|%203.12-0366d6)](https://www.python.org)

# Final Project BACKEND

create by : Dewa Surya Ariesta

hosting :[hosting on railway ](https://revou-finalproject-backend-production.up.railway.app/)

## environment variable needed

- `CLOUDINARY_URL`

  get the `CLOUDINARY_URL` from cloudinary
  ![cloudinary_dashboard](/screenshots/clodinary_dashboard.png)

- `FLASK_DEBUG` just put `FLASK_DEBUG= True` so the app run on development mode

## run the project

1. `poetry install` # install the dependency

2. `poetry run flask run` or `script/flask_run.bat` for windows # run the app
3. `poetry run pytest -s` or `script/test.bat` for windows # test the app
4. `poetry run pytest --cov` or `script/cov.bat` for windows # see test coverage
5. `poetry show --tree` # show all dependency use on this app

## Api document appearance

- Default document use [redocj](https://github.com/Redocly/redoc)

![image](/screenshots/api_document.png)

- Another document write by rapidcoc [final_project_rapidoc](https://revou-finalproject-backend-production.up.railway.app/api/rapidoc)

![image_rapidoc](/screenshots/rapidoc_document.png)

## folder structure

```txt
app
   |-- __init__.py
   |-- database_connector
   |-- datetime_service
   |-- final_project_api        # the app logic get mapped
   |   |-- business_module
   |   |-- product_module
   |   |-- user_module
   |   |-- conftest.py
   |   |-- main.py
   |-- image_upload_service
   |-- jwt_service
   |-- message_service
   |-- model_base_service
```
