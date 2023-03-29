from typing import Dict, Any

from flask import Response
from tinydb import Query, TinyDB

from handlers.calculators.transaction_calculator import TransactionCalculator


class TransactionHandler:

    def __init__(self, request_args: dict) -> None:
        self.rental_day_count: int = int(request_args["rental_day_count"])
        self.discount_percent: int = int(request_args["discount_percent"])
        self.tool_code: str = request_args["tool_code"]
        self.check_out_date: str = request_args["check_out_date"]

    def handle(self):

        try:
            self._check_for_errors()
        except ValueError as exc:
            return Response(
                str(exc),
                status=400
            )

        db = TinyDB('tinydb.json')
        existing_tool = Query()
        db_tool = db.search(existing_tool.code == self.tool_code)

        return TransactionCalculator(
            db_tool,
            self.rental_day_count,
            self.discount_percent,
            self.tool_code,
            self.check_out_date).calculate()

    def _check_for_errors(self):
        if self.rental_day_count < 1:
            raise ValueError(f"Rental day count {self.rental_day_count} is invalid, should be 1 or greater")
        if self.discount_percent < 0 or self.discount_percent > 100:
            raise ValueError(
                f"Discount percent {self.discount_percent} is invalid, should be between 0 and 100")

        # check if in db
        db = TinyDB('tinydb.json')
        existing_tool = Query()
        result = db.search(existing_tool.code == self.tool_code)
        if not result:
            raise ValueError(
                f"No tools with code {self.tool_code} exist in database"
            )
