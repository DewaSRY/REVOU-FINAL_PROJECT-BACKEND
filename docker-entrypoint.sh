#!/bin/sh


exec poetry run waitress-serve --host 0.0.0.0 --call app:create_app