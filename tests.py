from http.client import HTTPConnection
import json
import os
import base64

if os.path.exists('chat.db'):
    os.remove('chat.db')

def create_conn():
    return HTTPConnection("localhost", 8000)


def test_create_and_get_user():
    conn = create_conn()
    user_data = {"name": "testuser1", "password": "testuser123", "email": "testuser@test.com"}
    conn.request('POST',
                 '/admin/users',
                 json.dumps(user_data),
                 {'Authorization': 'Basic YWRtaW46MTIzNDU2Nzg=', 'Content-Type': 'application/json'
                  })
    resp = conn.getresponse()
    resp = resp.read().decode()
    resp = json.loads(resp)
    for k in user_data:
        if k == 'password':
            continue
        assert resp[k] == user_data[k]
    print(resp)
    # test get
    conn.request('GET',
                 f'/admin/users/{resp["id"]}',
                 json.dumps(user_data),
                 {'Authorization': 'Basic YWRtaW46MTIzNDU2Nzg='
                  })
    get_resp = conn.getresponse().read().decode()
    get_resp = json.loads(get_resp)
    for k in resp:
        assert resp[k] == get_resp[k]

def test_create_group():
    conn = create_conn()
    user_data = {"name": "group1"}
    conn.request('POST',
                 '/group',
                 json.dumps(user_data),
                 {'Authorization': f'Basic {base64.b64encode("1:testuser123".encode()).decode()}', 'Content-Type': 'application/json'
                  })
    # group created adds the creating user as member
    user_data['members'] = [1]
    resp = conn.getresponse()
    resp = resp.read().decode()
    print(resp)
    resp = json.loads(resp)
    for k in user_data:
        assert resp[k] == user_data[k]
    print(resp)


test_create_and_get_user()
test_create_group()