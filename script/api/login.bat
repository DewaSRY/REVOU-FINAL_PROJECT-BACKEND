@echo off


curl -X 'POST' \
  'http://localhost:5000/api/user/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "string",
  "password": "string",
  "email": "user@example.com"
}'