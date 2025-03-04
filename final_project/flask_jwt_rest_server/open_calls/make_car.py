from flask import request, g, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import jwt
from tools.logging import logger

def handle_request():
     car_name = request.form['carname']
     car_vin = request.form['carvin']
     car_price = request.form['carprice']
     secret = 'secret'
     logger.debug("Making New Car Handle Request")
     cur = g.db.cursor()
     cur.execute(f"INSERT INTO cars(name,vin, price) VALUES('{car_name}','{car_vin}','{car_price}');")
     g.db.commit()
     logger.debug("New Car Added")
     car = []
     data = {
            "car" : car_name, #sub is used by pyJwt as the owner of the token                                                                                                                                                         
            "vin" : car_vin,
            "price": car_price
     }
     car.append(data)
     jwt_str = jwt.encode(data ,secret, algorithm="HS256")
     #jwt_str = jwt.encode(add_car ,secret, algorithm="HS256")                                                                                                                                                                        
     return jsonify({'data':data,'message' : 'VALID USER, TOKEN IS SENT', 'token' : jwt_str})
     #return json_response( token = create_token(  g.jwt_data ) , car = car)  
