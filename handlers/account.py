import tornado.web
import hashlib
import json
from handlers.base import BaseHandler


class AccountHandler(BaseHandler):
    def initialize(self, db):
        super().initialize(db)

    def get(self):
        self.render("account_create.html")

    def post(self):
        if self.get_body_arguments("username") != [] and self.get_body_arguments("password") != []:
            username = self.get_body_argument("username")
            password = self.get_body_argument("password")
            if username and password:
                users = self.db['users']
                lists = self.db['lists']
                if users.find_one({'username': username}):
                    self.write_response_bad(error_msg="User already exists")
                else:
                    hashed_pass = hashlib.md5(password.encode("utf-8")).hexdigest()
                    users.insert_one({'username': username, 'password': hashed_pass, 'is_admin': False, 'is_active': True})
                    lists.insert_one({'list_name':"Default", 'username': username, 'share_link': ""})
                    self.set_current_user(username)
                    self.write_response_created()
            else:
                self.write_response_bad(error_msg="Invalid username or password")
        else:
            self.write_response_bad(error_msg="Username or password not provided")

            
