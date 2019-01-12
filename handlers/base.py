import tornado.web
import json
import traceback


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def get_current_session(self):
        return self.get_current_user(), self.get_current_list()

    def set_current_session(self, user, list_id):
        self.set_secure_cookie("user", user)
        self.set_secure_cookie("list_id", list_id)

    def clear_current_session(self):
        self.set_current_session("", "")

    def get_current_user(self):
        return self.get_secure_cookie("user").decode("utf-8") if self.get_secure_cookie("user") else None

    def set_current_user(self, user):
        self.set_secure_cookie("user", user)

    def get_current_list(self):
        return self.get_secure_cookie("list_id").decode("utf-8") if self.get_secure_cookie("list_id") else None

    def set_current_list(self, list_id):
        self.set_secure_cookie("list_id", str(list_id))

    def write_error(self, status_code, **kwargs):
        if 'exc_info' in kwargs:
            err_cls, err, traceback = kwargs['exc_info']
        errorMsg = err if err else ""
        self.render("error.html", code=status_code, message=errorMsg)
        
    def write_response(self, status_code, **kwargs):
        response = {}
        response['status'] = status_code
        for key in kwargs:
            response[key] = kwargs[key]
        if 'errorMsg' not in response:
            response['errorMsg'] = None
        self.set_header("Content-Type", "application/json")
        self.set_status(status_code)
        self.write(json.dumps(response))

    def write_response_ok(self, **kwargs):
        self.write_response(200, **kwargs)
        
    def write_response_created(self, **kwargs):
        self.write_response(201, **kwargs)

    def write_response_bad(self, **kwargs):
        self.write_response(400, **kwargs)
        
    def write_response_forbidden(self, **kwargs):
        self.write_response(403, **kwargs)

    def write_response_not_found(self, **kwargs):
        self.write_response(404, **kwargs)


class ErrorHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.render("404.html")


def authenticated(func):
    def _func(self, *args, **kwargs):
        if self.get_current_user() is None:
            self.write_response_forbidden(errorMsg="Not logged in", redirectUrl="/p/login")
        else:
            func(self, *args, **kwargs)
    return _func


