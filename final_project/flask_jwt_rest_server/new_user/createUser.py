from flask import request, g, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from db_con import get_db, get_db_instance
from tools.logging import logger
from new_user.salt import salt_pass
import bcrypt, jwt
from tools.token_required import token_required

#userPass = bytes(userPass,"utf-8")
def CreateUser(user_id,user,user_pass):
    #Insert into users(id,username,password) Values ('10','sdklfsdhjkfldf','fasdfgsgsdg');
    logger.debug("Adding New User As Requested")
    secret = 'secret'
    #encrypt_pass = bytes(user_pass,"utf-8")
    # enc_pass = salt_pass(user_pass)
    #str(enc_pass)
    #user_pass = bytes(user_pass,"utf-8") 
    cur = g.db.cursor()
    cur.execute(f"INSERT INTO users(id,username, password) VALUES({user_id},'{user}','{user_pass}');")
    g.db.commit()
    logger.debug('USER HAS BEEN SUCCESSFULLY ADDED TO DB')
    # user_pass = bytes(user_pass,"utf-8")
    #user_pass = user_pass.encode('utf-8')
   
    # enc_pass = encrypt_pass.encode('utf-8')
    user = {
            "username" : user, #sub is used by pyJwt as the owner of the token                                                       
            "password" : user_pass
        }
    logger.debug('SUCCESS, User is Valid and ADDED')
        
    jwt_str = jwt.encode(user ,secret, algorithm="HS256")
    print('ENCODED USER: ',jwt_str)
    print('JWT: ',jwt_str)
    logger.debug(jsonify({'message' : 'VALID USER, TOKEN IS SENT', 'token' : jwt_str}))                                               \

    return jsonify({'message' : 'VALID USER, TOKEN IS SENT', 'token' : jwt_str}) 



    #return json_response( token = create_token(  g.jwt_data ) , cars = cars)


    
