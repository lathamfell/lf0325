# initialize the prod db according to the specification
rm tinydb.json;
curl --location 'http://127.0.0.1:5000/tool/add' \
--header 'Content-Type: application/json' \
--data '{
    "code": "CHNS",
    "type": "Chainsaw",
    "brand": "Stihl"
}'
curl --location 'http://127.0.0.1:5000/tool/add' \
--header 'Content-Type: application/json' \
--data '{
    "code": "LADW",
    "type": "Ladder",
    "brand": "Werner"
}'
curl --location 'http://127.0.0.1:5000/tool/add' \
--header 'Content-Type: application/json' \
--data '{
    "code": "JAKD",
    "type": "Jackhammer",
    "brand": "DeWalt"
}'
curl --location 'http://127.0.0.1:5000/tool/add' \
--header 'Content-Type: application/json' \
--data '{
    "code": "JAKR",
    "type": "Jackhammer",
    "brand": "Ridgid"
}'
curl --location --request PUT 'http://127.0.0.1:5000/tool/update' \
--header 'Content-Type: application/json' \
--data '{
    "type": "Ladder",
    "daily_charge": "1.99",
    "weekday_charge": true,
    "weekend_charge": true,
    "holiday_charge": false
}'
curl --location --request PUT 'http://127.0.0.1:5000/tool/update' \
--header 'Content-Type: application/json' \
--data '{
    "type": "Chainsaw",
    "daily_charge": "1.49",
    "weekday_charge": true,
    "weekend_charge": false,
    "holiday_charge": true
}'
curl --location --request PUT 'http://127.0.0.1:5000/tool/update' \
--header 'Content-Type: application/json' \
--data '{
    "type": "Jackhammer",
    "daily_charge": "2.99",
    "weekday_charge": true,
    "weekend_charge": false,
    "holiday_charge": false
}'