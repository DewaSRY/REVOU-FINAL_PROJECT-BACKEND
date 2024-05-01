@echo off

poetry run waitress-serve --host 127.0.0.1 --call app:create_app