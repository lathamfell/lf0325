from typing import Union

from flask import Response
from tinydb import Query, TinyDB


class UpdateToolHandler:

    def __init__(self):
        pass

    @staticmethod
    def handle(request_json: dict) -> Union[Response, str]:
        # check if in db
        db = TinyDB('tinydb.json')
        tool_type = request_json['type']
        existing_tool = Query()
        result = db.search(existing_tool.type == tool_type)
        if not result:
            return Response(
                f"No tools with type {tool_type} exist in database",
                status=404
            )
        else:
            # update in db
            tool_update = request_json
            if tool_update.get('daily_charge'):
                db.update({'daily_charge': tool_update['daily_charge']}, existing_tool.type == tool_type)
            if tool_update.get('weekend_charge') is not None:
                db.update({'weekend_charge': tool_update['weekend_charge']}, existing_tool.type == tool_type)
            if tool_update.get('weekday_charge') is not None:
                db.update({'weekday_charge': tool_update['weekday_charge']}, existing_tool.type == tool_type)
            if tool_update.get('holiday_charge') is not None:
                db.update({'holiday_charge': tool_update['holiday_charge']}, existing_tool.type == tool_type)
            return "Tool updated"
