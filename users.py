class User:

    def __init__(self, id, name, password, email):
        self.user_id = id
        self.user_name = name
        self.password = password
        self.email_id = email

    def to_dict(self):
        return {'id': self.user_id, 'name': self.user_name, 'email': self.email_id}


class Group:

    def __init__(self, id, name, members=[]):
        self.group_name = name
        self.group_id = id
        self.members = members

    def to_dict(self):
        return {'id': self.group_id, 'name': self.group_name, 'members': self.members}
