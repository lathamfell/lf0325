from typing import Union

from flask import Response
from tinydb import Query, TinyDB

from tool import Tool


class AddToolHandler:

    def __init__(self):
        pass

    @staticmethod
    def handle(request_json: dict) -> Union[Response, str]:
        # create tool obj
        new_tool = Tool()
        new_tool.type = request_json['type']
        new_tool.code = request_json['code']
        new_tool.brand = request_json['brand']
        # check if code already in db
        existing_tool = Query()
        db = TinyDB('tinydb.json')
        result = db.search(existing_tool.code == new_tool.code)
        if not result:
            # save in db
            db.insert({'code': new_tool.code, 'type': new_tool.type, 'brand': new_tool.brand})
            return f"Tool {new_tool.code} inserted"
        else:
            return Response(
                f"Tool with code {new_tool.code} already exists in database",
                status=409
            )
