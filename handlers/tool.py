import handlers.tool


class Tool:
    def __init__(self: handlers.tool.Tool):
        self.daily_charge: str
        self.weekend_charge: bool = False
        self.weekday_charge: bool = False
        self.holiday_charge: bool = False
        self.type: str
        self.code: str
        self.brand: str
