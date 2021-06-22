from flask import Flask, request, Response
import json
import base64
from users import *
from chat_db import ChatDB

app = Flask(__name__)
admin = 'admin'
password = '12345678'
messages = {}


def extract_items(auth_header):
    encoded_str = auth_header.split()[1]
    decoded_bytes = base64.urlsafe_b64decode(encoded_str)
    decoded_str = str(decoded_bytes, "utf-8")
    root_user = decoded_str.split(':')[0]
    root_pwd = decoded_str.split(':')[1]
    return root_user, root_pwd


def authenticate_admin(auth_header):
    root_user, root_pwd = extract_items(auth_header)
    return root_pwd == password and root_user == admin


def authenticate_user(auth_header):
    db = ChatDB("chat.db")
    uid, pwd = extract_items(auth_header)
    user = db.get_user(uid)
    return user.password == pwd


@app.route('/admin/users', methods=['POST'])
def create_user():
    db = ChatDB("chat.db")
    json_header = request.headers["Authorization"]
    if authenticate_admin(json_header):
        json_data = request.json
        user_obj = db.create_user(json_data["name"], json_data["email"], json_data["password"])
        return user_obj.to_dict()
    else:
        return Response("authentication failed to create user", status=401)


@app.route('/admin/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    db = ChatDB("chat.db")
    json_header = request.headers["Authorization"]
    if not authenticate_admin(json_header):
        return Response("authentication failed to edit", status=401)
    json_data = request.json
    try:
        user = db.get_user(user_id)
        for key in json_data:
            if key == "email":
                user.email_id = json_data[key]
            elif key == "name":
                user.user_name = json_data[key]
        user = db.update_user(user)
        return user.to_dict()
    except Exception as e:
        return Response(f"user with id {user_id} is not available", status=404)


@app.route('/admin/users/<int:user_id>', methods=['GET'])
def get_details(user_id):
    db = ChatDB("chat.db")
    json_header = request.headers["Authorization"]
    if not authenticate_admin(json_header):
        return Response("authentication failed to get details", status=401)
    try:
        return db.get_user(user_id).to_dict()
    except:
        return Response(f"no user with id {user_id}", status=404)


@app.route('/group', methods=['POST'])
def create_group():
    db = ChatDB("chat.db")
    json_header = request.headers["Authorization"]
    if not authenticate_user(json_header):
        return Response('Not a valid user', status=404)
    user = db.get_user(extract_items(json_header)[0])
    json_data = request.json
    group_obj = db.create_group(json_data["name"])
    db.add_member_to_group(group_obj.group_id, user.user_id)
    group_obj = db.get_group(group_obj.group_id)
    messages[group_obj.group_id] = {str(user.user_id): []}
    return group_obj.to_dict()


@app.route('/group/<int:group_id>', methods=['PUT'])
def add_member(group_id):
    db = ChatDB("chat.db")
    json_header = request.headers["Authorization"]
    json_data = request.json
    if not authenticate_user(json_header):
        return Response('Not a valid user', status=404)
    try:
        group = db.get_group(group_id)
        for i in json_data:
            db.add_member_to_group(group.group_id, i)
            if str(i) not in messages[group.group_id]:
                messages[group.group_id][str(i)] = []
        return db.get_group(group_id).to_dict()
    except:
        return Response(status=404)


@app.route('/group/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    db = ChatDB("chat.db")
    json_header = request.headers["Authorization"]
    items_in_header = extract_items(json_header)
    user_id = items_in_header[0]
    if not authenticate_user(json_header):
        return Response('authentication failed', status=401)
    try:
        group = db.get_group(group_id)
        if user_id in group.members:
            db.remove_group(group_id)
            messages.pop(group.group_id)
            return Response(status=204)
        return Response('not a member of this group', status=404)
    except:
        return Response(status=404)


@app.route('/search', methods=['GET'])
def search():
    db = ChatDB("chat.db")
    search_var = request.args.get("name")
    json_header = request.headers["Authorization"]
    if not authenticate_user(json_header):
        return Response(status=401)

    f_list = []
    users = db.get_users()
    for user in users:
        if search_var in user.user_name:
            f_list.append(user.to_dict())
    return {'results': f_list}


@app.route('/group/<int:group_id>/messages', methods=['POST'])
def send_msgs(group_id):
    db = ChatDB("chat.db")
    json_header = request.headers["Authorization"]
    id_in_header = extract_items(json_header)[0]
    print(id_in_header)
    if not authenticate_user(json_header):
        return Response('User not in group', status=401)
    print(f'gid{group_id}')
    group = db.get_group(group_id)
    members = group.members
    message = request.json["message"]
    # { "message": "hello" }
    for member in messages[group.group_id]:
        if member != id_in_header:
            messages[group.group_id][member].append(message)
    return Response(status=200)


@app.route('/group/<int:group_id>/messages', methods=['GET'])
def get_msgs(group_id):
    db = ChatDB("chat.db")
    json_header = request.headers["Authorization"]
    id_in_header = extract_items(json_header)[0]
    if not authenticate_user(json_header):
        return Response('Invalid user', status=401)
    group = db.get_group(group_id)
    print(group.members)
    if int(id_in_header) not in group.members:
        return Response('not a member', status=401)
    queued_msgs = messages[group.group_id][id_in_header]
    messages[group.group_id][id_in_header] = []
    return {'messages': queued_msgs}


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=8000)



