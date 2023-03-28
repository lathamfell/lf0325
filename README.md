# lf0325

# Instructions

Note these instructions are for OSX / Linux, Windows may require different commands.

Create a venv:
`python3 -m ./venv`

Start the venv:
`source ./venv/bin/activate`

If permission is denied to ./venv/bin/activate, add execute permissions:
`chmod +x ./venv/bin/activate`

Install dependencies:
`pip3 install -r requirements.txt`

Start the flask server:
`flask --app api.py run`

Initialize the prod database:
`./initialize_prod_db.sh`

Add the new ladder tool:
`curl --location 'http://127.0.0.1:5000/tool/add' \
--header 'Content-Type: application/json' \
--data '{
    "code": "LADX",
    "type": "Ladder",
    "brand": "LittleGiant"
}'`

Update the daily ladder charge:
`curl --location --request PUT 'http://127.0.0.1:5000/tool/update' \
--header 'Content-Type: application/json' \
--data '{
    "type": "Ladder",
    "daily_charge": "2.99",
    "weekday_charge": true,
    "weekend_charge": true,
    "holiday_charge": false
}'`

Fetch the following five transactions and check the results:

Transaction for JAKR:
`curl --location 'http://127.0.0.1:5000/transaction/submission?tool_code=JAKR&rental_day_count=5&discount_percent=101&check_out_date=2015-09-03' \
--data ''`

Result:
`Discount percent 101 is invalid, should be between 0 and 100`

Transaction for LADW:
`curl --location 'http://127.0.0.1:5000/transaction/submission?tool_code=LADW&rental_day_count=3&discount_percent=10&check_out_date=2020-07-02' \
--data ''`

Result:
`{
    "charge_days": 2,
    "check_out_date": "07/02/20",
    "daily_charge": "$2.99",
    "discount_amount": "$0.60",
    "discount_percent": "10%",
    "due_date": "07/05/20",
    "final_charge": "$5.38",
    "pre_discount_charge": "$5.98",
    "rental_day_count": 3,
    "tool_brand": "Werner",
    "tool_code": "LADW",
    "tool_type": "Ladder"
}`

Transaction for CHNS:
`curl --location 'http://127.0.0.1:5000/transaction/submission?tool_code=CHNS&rental_day_count=5&discount_percent=25&check_out_date=2015-07-02' \
--data ''`

Result:
`{
    "charge_days": 3,
    "check_out_date": "07/02/15",
    "daily_charge": "$1.49",
    "discount_amount": "$1.12",
    "discount_percent": "25%",
    "due_date": "07/07/15",
    "final_charge": "$3.35",
    "pre_discount_charge": "$4.47",
    "rental_day_count": 5,
    "tool_brand": "Stihl",
    "tool_code": "CHNS",
    "tool_type": "Chainsaw"
}`

Transaction for JAKD:
`curl --location 'http://127.0.0.1:5000/transaction/submission?tool_code=JAKD&rental_day_count=6&discount_percent=0&check_out_date=2015-09-03' \
--data ''`

Result:
`
    "charge_days": 3,
    "check_out_date": "09/03/15",
    "daily_charge": "$2.99",
    "discount_amount": "$0.00",
    "discount_percent": "0%",
    "due_date": "09/09/15",
    "final_charge": "$8.97",
    "pre_discount_charge": "$8.97",
    "rental_day_count": 6,
    "tool_brand": "DeWalt",
    "tool_code": "JAKD",
    "tool_type": "Jackhammer"
}`

Transaction for JAKR (second transaction):
`curl --location 'http://127.0.0.1:5000/transaction/submission?tool_code=JAKR&rental_day_count=9&discount_percent=0&check_out_date=2015-07-02' \
--data ''`

Result:
`{
    "charge_days": 6,
    "check_out_date": "07/02/15",
    "daily_charge": "$2.99",
    "discount_amount": "$0.00",
    "discount_percent": "0%",
    "due_date": "07/11/15",
    "final_charge": "$17.94",
    "pre_discount_charge": "$17.94",
    "rental_day_count": 9,
    "tool_brand": "Ridgid",
    "tool_code": "JAKR",
    "tool_type": "Jackhammer"
}`

Transaction for LADL:
`curl --location 'http://127.0.0.1:5000/transaction/submission?tool_code=LADL&rental_day_count=4&discount_percent=50&check_out_date=2020-07-02' \
--data ''`

Result:
`No tools with code LADL exist in database`

# mypy

Run mypy to check types: `mypy handlers api.py tool.py`
