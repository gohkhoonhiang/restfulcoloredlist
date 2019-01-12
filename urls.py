from tornado.web import url
from handlers.main import MainHandler
from handlers.list import ListItemHandler, ListItemListHandler, \
                            ListItemPageHandler
from handlers.auth import LoginHandler, LoginPageHandler, LogoutHandler
from handlers.account import AccountHandler, AccountListHandler, \
                            AccountCreatePageHandler, AccountViewPageHandler
from db import db


url_patterns = [
    url(r"/", MainHandler, dict(db=db)),
    url(r"/items/([0-9a-zA-Z\-]+)", ListItemHandler, dict(db=db)),
    url(r"/items", ListItemListHandler, dict(db=db)),
    url(r"/p/items", ListItemPageHandler, dict(db=db)),
    url(r"/login", LoginHandler, dict(db=db)),
    url(r"/p/login", LoginPageHandler, dict(db=db)),
    url(r"/logout", LogoutHandler, dict(db=db)),
    url(r"/accounts/([0-9a-zA-Z\-]+)", AccountHandler, dict(db=db)),
    url(r"/accounts", AccountListHandler, dict(db=db)),
    url(r"/p/account/create", AccountCreatePageHandler, dict(db=db)),
    url(r"/p/account/view", AccountViewPageHandler, dict(db=db)),
]


