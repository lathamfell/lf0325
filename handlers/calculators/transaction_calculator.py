import calendar

from datetime import datetime, timedelta, date

from flask import jsonify


class TransactionCalculator:

    def __init__(self,
                 db_tool,
                 rental_day_count,
                 discount_percent,
                 tool_code,
                 check_out_date,
                 ):
        self.db_tool = db_tool
        self.rental_day_count: int = rental_day_count
        self.discount_percent: int = discount_percent
        self.tool_code: str = tool_code
        self.check_out_date: str = check_out_date

        self.weekday_charge: bool
        self.weekend_charge: bool
        self.holiday_charge: bool
        self.charge_days: int
        self.check_out_date_dt: date
        self.due_date: str
        self.db_tool: str
        self.tool_type: str
        self.tool_brand: str
        self.daily_charge: str
        self.final_charge: float
        self.pre_discount_charge: float
        self.discount_amount: float
        self.cur_date: date
        self.day_is_weekday: bool
        self.day_is_weekend: bool
        self.day_is_monday: bool
        self.day_is_friday: bool

    def calculate(self):
        self._save_result_attributes()

        self._calculate_due_date()

        self._calculate_charge_days()

        self._calculate_final_charge()

        data = {
            "tool_code": self.tool_code,
            "tool_type": self.tool_type,
            "tool_brand": self.tool_brand,
            "rental_day_count": self.rental_day_count,
            "check_out_date": self.check_out_date_dt.strftime("%m/%d/%y"),
            "due_date": self.due_date.strftime("%m/%d/%y"),
            "daily_charge": "${:,.2f}".format(float(self.daily_charge)),
            "charge_days": self.charge_days,
            "pre_discount_charge": "${:,.2f}".format(self.pre_discount_charge),
            "discount_percent": f"{self.discount_percent}%",
            "discount_amount": "${:,.2f}".format(self.discount_amount),
            "final_charge": "${:,.2f}".format(self.final_charge)
        }
        return jsonify(data)

    def _save_result_attributes(self):
        self.tool_type = self.db_tool[0]['type']
        self.tool_brand = self.db_tool[0]['brand']
        self.weekday_charge = self.db_tool[0]['weekday_charge']
        self.weekend_charge = self.db_tool[0]['weekend_charge']
        self.holiday_charge = self.db_tool[0]['holiday_charge']
        self.daily_charge = self.db_tool[0]['daily_charge']

    def _calculate_due_date(self):
        self.check_out_date_dt = datetime.strptime(self.check_out_date, '%Y-%m-%d')
        self.due_date = self.check_out_date_dt + timedelta(days=self.rental_day_count)

    def _calculate_charge_days(self):
        self.cur_date = self.check_out_date_dt
        self.charge_days = self.rental_day_count
        for i in range(self.rental_day_count):  # runs once for each day in rental period
            self.day_is_weekday = self.cur_date.weekday() in [0, 1, 2, 3, 4]
            self.day_is_weekend = self.cur_date.weekday() in [5, 6]
            self.day_is_monday = self.cur_date.weekday() == 0
            self.day_is_friday = self.cur_date.weekday() == 4

            day_is_holiday = self._day_is_holiday()

            if not self.weekday_charge and self.day_is_weekday:
                self.charge_days -= 1
            elif not self.weekend_charge and self.day_is_weekend:
                self.charge_days -= 1
            elif not self.holiday_charge and day_is_holiday:
                self.charge_days -= 1
            else:
                pass  # this day is charged
            self.cur_date = self.cur_date + timedelta(days=1)

    def _day_is_holiday(self):
        day_is_labor_day = self._get_labor_day(self.cur_date.year) == self.cur_date.date()

        day_is_fourth_of_july_holiday = False
        day_is_fourth_of_july = date(self.cur_date.year, 7, 4) == self.cur_date.date()
        day_is_third_of_july = date(self.cur_date.year, 7, 3) == self.cur_date.date()
        day_is_fifth_of_july = date(self.cur_date.year, 7, 5) == self.cur_date.date()
        # if it's fourth of july and a weekday, then it's the 4th of July holiday
        if day_is_fourth_of_july and self.day_is_weekday:
            day_is_fourth_of_july_holiday = True
        if self.day_is_friday and day_is_third_of_july:
            # tomorrow is Sat the 4th of July, so today is a holiday
            day_is_fourth_of_july_holiday = True
        if self.day_is_monday and day_is_fifth_of_july:
            # yesterday was Sun the 4th of July, so today is a holiday
            day_is_fourth_of_july_holiday = True
        day_is_holiday = day_is_labor_day or day_is_fourth_of_july_holiday
        return day_is_holiday

    def _calculate_final_charge(self):
        self.pre_discount_charge = self.charge_days * float(self.daily_charge)
        self.discount_amount = self.discount_percent * 0.01 * self.pre_discount_charge
        self.final_charge = self.pre_discount_charge - self.discount_amount

    @staticmethod
    def _get_labor_day(year):
        month = 9
        mycal = calendar.Calendar(0)
        cal = mycal.monthdatescalendar(year, month)
        if cal[0][0].month == month:
            return cal[0][0]
        else:
            return cal[1][0]
