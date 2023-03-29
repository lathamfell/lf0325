from typing import Union, Dict, Any

from handlers.transaction_handler import TransactionHandler
from handlers.add_tool_handler import AddToolHandler
from flask import Flask, request, Response, jsonify

from handlers.update_tool_handler import UpdateToolHandler

app = Flask(__name__)


@app.route("/tool/add", methods=["POST"])
def add_tool() -> Union[Response, str]:
    assert isinstance(request.json, dict)  # mypy necessity
    return AddToolHandler().handle(request.json)


@app.route("/tool/update", methods=["PUT"])
def update_tool() -> Union[Response, str]:
    assert isinstance(request.json, dict)  # mypy necessity
    return UpdateToolHandler().handle(request.json)


@app.route("/transaction/submission", methods=["GET"])
def submit_transaction() -> Response:
    return jsonify(TransactionHandler(request.args).handle())
