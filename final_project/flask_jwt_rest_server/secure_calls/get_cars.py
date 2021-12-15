from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Get Cars Handle Request")
    cur = g.db.cursor()
    cur.execute("select * from cars")
    cars = []
    for r in cur.fetchall():
        print('Cars: ',r)
        cars_dict = {"car": r[0], "vin":r[1], "price":r[2]}
        cars.append(cars_dict)
    return json_response( token = create_token(  g.jwt_data ) , cars = cars)

