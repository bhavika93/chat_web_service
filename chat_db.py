import sqlite3
from users import *

class ChatDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        create_users_table_query = '''CREATE TABLE IF NOT EXISTS users
                        (id INTEGER PRIMARY KEY,
                         name TEXT NOT NULL,
                         password TEXT NOT NULL,
                         email TEXT NOT NULL UNIQUE)'''

        create_groups_table_query = '''CREATE TABLE IF NOT EXISTS groups
                        (id INTEGER PRIMARY KEY,
                         name TEXT NOT NULL)'''

        create_members_table_query = '''CREATE TABLE IF NOT EXISTS members
                        (gid INTEGER NOT NULL,
                         uid INTEGER NOT NULL,
                         FOREIGN KEY (gid) REFERENCES groups (id),
                         FOREIGN KEY (uid) REFERENCES users (id),
                         PRIMARY KEY (gid,uid))'''

        self.cursor.execute(create_users_table_query)
        self.cursor.execute(create_groups_table_query)
        self.cursor.execute(create_members_table_query)

        self.conn.commit()

    def create_user(self, name, email, password):
        insert_query = f'''INSERT INTO users (name, email, password)
            VALUES ("{name}", "{email}", "{password}")'''
        self.cursor.execute(insert_query)
        self.conn.commit()
        select_query = f'''SELECT *  FROM users WHERE email="{email}"'''
        self.cursor.execute(select_query)
        user = next(self.cursor)
        return User(*user)

    def get_user(self, id):
        select_query = f'''SELECT *  FROM users WHERE id={id}'''
        self.cursor.execute(select_query)
        user = next(self.cursor)
        return User(*user)

    def get_users(self):
        select_query = f'''SELECT * FROM users'''
        self.cursor.execute(select_query)
        return list(map(lambda x: User(*x), self.cursor))

    def update_user(self, userobj):
        update_query = f'''UPDATE users SET
                        name = "{userobj.user_name}",
                        email = "{userobj.email_id}",
                        password = "{userobj.password}"
                        WHERE id = {userobj.user_id}'''
        self.cursor.execute(update_query)
        self.conn.commit()
        select_query = f'''SELECT * FROM users WHERE id={userobj.user_id}'''
        self.cursor.execute(select_query)
        user = next(self.cursor)
        return User(*user)

    def create_group(self, name):
        insert_query = f'''INSERT INTO groups (name)
            VALUES ("{name}")'''
        self.cursor.execute(insert_query)
        self.conn.commit()
        select_query = f'''SELECT *  FROM groups ORDER BY id DESC LIMIT 1'''
        self.cursor.execute(select_query)
        group = next(self.cursor)
        # print(group)
        return Group(*group)

    def get_group(self, gid):
        select_query = f'''SELECT *  FROM groups WHERE id={gid}'''
        self.cursor.execute(select_query)
        group = next(self.cursor)
        # print(group)
        g = Group(*group)
        g.members = self.get_members_of_group(g.group_id)
        return g

    def remove_group(self, gid):
        delete_query = f'''DELETE FROM groups WHERE id={gid}'''
        self.cursor.execute(delete_query)
        self.conn.commit()

    def add_member_to_group(self, gid, uid):
        insert_query = f'''INSERT INTO members (gid, uid)
            VALUES ({gid}, {uid})'''
        self.cursor.execute(insert_query)
        self.conn.commit()

    def get_members_of_group(self, gid):
        insert_query = f'''SELECT uid FROM members WHERE gid={gid}'''
        self.cursor.execute(insert_query)
        return list(map(lambda x: x[0], self.cursor))



