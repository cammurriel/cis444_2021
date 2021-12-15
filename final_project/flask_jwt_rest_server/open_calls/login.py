from flask import request, g, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from tools.token_required import token_required
import bcrypt, jwt
from tools.logging import logger
from db_con import get_db_instance, get_db
from tools.get_aws_secrets import get_secrets
from new_user.createUser import CreateUser
import random
def handle_request():
    secrets = get_secrets
    logger.debug("Login Handle Request")
    global_db_con = get_db()
    cur =g.db.cursor()
    id_num = random.randint(10,1000)
    user_input = request.form['firstname']
    password_input = request.form['password']
    secret = 'secret'
    #making secret into byte format
    #secret = bytes(secret,"utf-8")

    ''' querying the db and checking if a user is there'''
    cur.execute(f"SELECT * FROM users WHERE username = '{user_input}';")
    userData = cur.fetchone()

    if userData is None:
        logger.debug('USEROW IS NONE')
       # password_input = bytes(user_input ,"utf-8") 
        return CreateUser(id_num , user_input,password_input)
        #jwt_str = jwt.encode(new_user ,secret, algorithm="HS256")
        #return jsonify({"message" : "INVALID INPUT", 'token' : None})
    else:
        logger.debug('DB FOUND SOMETHING')
        userPass = userData[2]
        print(userPass)
        userPass = bytes(userPass,"utf-8")
        print ('user password: ',userPass)
        isUserValid = bcrypt.checkpw(bytes(password_input,('utf-8')),userPass)
        

        if isUserValid:
            user = {                                                                                          
            "username" : user_input, #sub is used by pyJwt as the owner of the token
            "password" : password_input                                                                                                   
            }  
            logger.debug('SUCCESS, User is Valid')

            jwt_str = jwt.encode(user ,secret, algorithm="HS256")
        
            print('ENCODED USER: ',jwt_str)
            print('JWT: ',jwt_str)                                                                                                      
            logger.debug(jsonify({'message' : 'VALID USER, TOKEN IS SENT', 'token' : jwt_str}))                                                
            return jsonify({'message' : 'VALID USER, TOKEN IS SENT', 'token' : jwt_str})                                               \
    
        else:         
             return jsonify({'message' : 'VALID USERNAME, Password is INCORRECT', 'token' : None})
   
       
