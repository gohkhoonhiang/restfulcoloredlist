import tornado.web
from bson.objectid import ObjectId
import json
from handlers.base import BaseHandler


class ListHandler(BaseHandler):
    def initialize(self, db):
        super().initialize(db)

    def get(self):
        username = self.get_current_user()
        if username:
            lists = self.db['lists']
            list_items = self.db['list_items']
            user_list = lists.find_one({'username': username})
            items = []
            if user_list:
                list_id = user_list['_id']
                self.set_current_list(list_id)
                items_cursor = list_items.find({'list_id': list_id})
                if items_cursor is not None:
                    items = [item for item in items_cursor]
            self.render("list.html", items=items)
        else:
            self.render("login.html")

    def post(self):
        username,list_id = self.get_current_session()
        if username and list_id:
            lists = self.db['lists']
            list_items = self.db['list_items']
            text = self.get_body_argument("text")
            if text:
                list_items.insert_one({'list_id': ObjectId(list_id), 'text':text, 'color':"Blue", 'status':"Open"})
            self.write_response_created()
        else:
            self.write_response_forbidden(error_msg="Please login to access your list")

    def put(self, item_id):
        username,list_id = self.get_current_session()
        if username and list_id:
            lists = self.db['lists']
            list_items = self.db['list_items']
            text = self.get_body_argument("text")
            if text:
                item = list_items.find({'_id': ObjectId(item_id)})
                if item:
                    list_items.update_one({'_id':ObjectId(item_id)}, {'$set':{'text':text}})
                    self.write_response_ok()
                else:
                    self.write_response_not_found(error_msg="Item not found")
            else:
                self.write_response_bad(error_msg="Empty list item text")
        else:
            self.write_response_forbidden(error_msg="Please login to access your list")

    def delete(self, item_id):
        username,list_id = self.get_current_session()
        if username and list_id:
            lists = self.db['lists']
            list_items = self.db['list_items']
            item = list_items.find({'_id': ObjectId(item_id)})
            if item:
                list_items.remove({'_id':ObjectId(item_id)})
                self.write_response_ok()
            else:
                self.write_response_not_found(error_msg="Item not found")
        else:
            self.write_response_forbidden(error_msg="Please login to access your list")


