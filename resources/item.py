from flask import Flask, request
import uuid
from db import ItemDatabase
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schema import ItemSchema, ItemGetSchema, SuccessMessageSchema, ItemQuerySchema, ItemOpetionalQuerySchema

blp = Blueprint("items", __name__, url_prefix="/item", description="Operations on Items")

@blp.route("/")
class Items(MethodView):

    def __init__(self):
        self.db = ItemDatabase()
    
    @blp.response(200, ItemGetSchema(many=True))
    @blp.arguments(ItemOpetionalQuerySchema, location="query")
    def get(self, args):
        id = args.get("id")
        if id is None:
            return self.db.get_items()
        
        else:
            result = self.db.get_item(id)
            if result is None:
                abort(404, message="Record doesn't exit!")
            return result

    @blp.arguments(ItemSchema)
    @blp.response(201, SuccessMessageSchema)
    def post(self, request_data):
        id = uuid.uuid4().hex
        self.db.add_item(id, request_data)
        return {"message": "Item added successfully"}, 201

    @blp.arguments(ItemSchema)
    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(ItemQuerySchema, location="query")
    def put(self, request_data, args):
        id = args.get('id')
        if self.db.update_item(id, request_data):
            return {"message":"Item updated successfully"}, 200
        abort(404, message="Item Not found!")

    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(ItemQuerySchema, location="query")
    def delete(self, args):
        id = args.get('id')
        if self.db.delete_item(id):
            return {"message" : "Record deleted successfuly"}, 200
        abort(404, message="Item Not found!")