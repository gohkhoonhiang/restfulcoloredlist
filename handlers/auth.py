import tornado.web
import json
import hashlib
from handlers.base import BaseHandler


class LoginHandler(BaseHandler):
    def initialize(self, db):
        super().initialize(db)

    def get(self):
        self.render("login.html")

    def post(self):
        if self.get_body_arguments("username") != [] and self.get_body_arguments("password") != []:
            username = self.get_body_argument("username")
            password = self.get_body_argument("password")
            users = self.db['users']
            if username and password:
                user = users.find_one({'username': username})
                if user:
                    stored_pass = user['password']
                    hashed_pass = hashlib.md5(password.encode("utf-8")).hexdigest()
                    if hashed_pass == stored_pass:
                        self.set_current_user(username)
                        self.write_response_ok()
                    else:
                        self.write_response_forbidden(error_msg="Invalid username or password")
                else:
                    self.write_response_forbidden(error_msg="Invalid username or password")
            else:
                self.write_response_forbidden(error_msg="Invalid username or password")
        else:
            self.write_response_bad(error_msg="Username or password not provided")

class LogoutHandler(BaseHandler):
    def initialize(self, db):
        super().initialize(db)

    def post(self):
        response = {}
        if self.get_current_user():
            self.clear_current_session()
            self.write_response_ok()
        else:
            self.clear_current_session()
            self.write_response_bad(error_msg="User not in session")


