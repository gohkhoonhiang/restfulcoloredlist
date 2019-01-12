from handlers.base import BaseHandler, authenticated


class MainHandler(BaseHandler):
    def initialize(self, db):
        super().initialize(db)

    @authenticated
    def get(self):
        self.write_response_ok(redirectUrl="/p/list")


