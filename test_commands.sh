#!/bin/bash
# creating users
curl  -X POST 'http://localhost:8000/admin/users' -H 'Content-Type: application/json' -H 'Authorization: Basic YWRtaW46MTIzNDU2Nzg=' -d '{"name":"abc","password":"abc123","email":"abc@test.com"}'
curl  -X POST 'http://localhost:8000/admin/users' -H 'Content-Type: application/json' -H 'Authorization: Basic YWRtaW46MTIzNDU2Nzg=' -d '{"name":"def","password":"def345","email":"def@test.com"}'
curl  -X POST 'http://localhost:8000/admin/users' -H 'Content-Type: application/json' -H 'Authorization: Basic YWRtaW46MTIzNDU2Nzg=' -d '{"name":"xyz","password":"xyz345","email":"xyz@test.com"}'
curl  -X POST 'http://localhost:8000/admin/users' -H 'Content-Type: application/json' -H 'Authorization: Basic YWRtaW46MTIzNDU2Nzg=' -d '{"name":"abcdef","password":"new12","email":"abcxyz@test.com"}'

# editing existing user with id
curl  -X PUT 'http://localhost:8000/admin/users/2' -H 'Content-Type: application/json' -H 'Authorization: Basic YWRtaW46MTIzNDU2Nzg=' -d '{"email":"new@new.com"}'

# getting details of user with id
curl  -X GET 'http://localhost:8000/admin/users/2' -H 'Content-Type: application/json' -H 'Authorization: Basic YWRtaW46MTIzNDU2Nzg='
curl  -X GET 'http://localhost:8000/admin/users/2' -H 'Content-Type: application/json' -u 'admin:12345678'

# creating group
curl  -X POST 'http://localhost:8000/group' -H 'Content-Type: application/json' -u '1:abc123' -d '{"name":"group1"}'
curl  -X POST 'http://localhost:8000/group' -H 'Content-Type: application/json' -u '1:abc123' -d '{"name":"group2"}'

# adding members to group with group id and user id
curl  -X PUT 'http://localhost:8000/group/1' -H 'Content-Type: application/json' -u '1:abc123' -d '["2","3"]'
curl  -X PUT 'http://localhost:8000/group/2' -H 'Content-Type: application/json' -u '1:abc123' -d '["3"]'
#curl  -X DELETE 'http://localhost:8000/group/1' -H 'Content-Type: application/json' -u '1:abc123'

# sending messages to group
curl  -X POST 'http://localhost:8000/group/1/messages' -H 'Content-Type: application/json' -u '1:abc123' -d '{"message": "hi"}'
curl  -X POST 'http://localhost:8000/group/1/messages' -H 'Content-Type: application/json' -u '1:abc123' -d '{"message": "hello"}'
curl  -X POST 'http://localhost:8000/group/1/messages' -H 'Content-Type: application/json' -u '1:abc123' -d '{"message": "bye"}'

# getting messages of users
curl  -X GET 'http://localhost:8000/group/1/messages' -H 'Content-Type: application/json' -u '1:abc123'
curl  -X GET 'http://localhost:8000/group/1/messages' -H 'Content-Type: application/json' -u '2:def345'

# searching
curl  -X GET 'http://localhost:8000/search?name=abc' -H 'Content-Type: application/json' -u '2:def345'

