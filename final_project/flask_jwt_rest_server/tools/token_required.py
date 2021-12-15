import jwt
from functools import wraps
from flask import request, redirect, g
from flask_json import FlaskJSON, JsonError, json_response, as_json

from tools.logging import logger

from tools.get_aws_secrets import get_secrets


def token_required(f): 
    @wraps(f)
    def _verify(*args, **kwargs):
        secrets = get_secrets
        secret = "secret"
        auth_headers = request.headers.get('Authorization', '').split(':')
        #auth_headers = request.json.get('Authorization', '').split(':')
        #logger.debug('REQUEST',request)
        #token = request.json.get('token')

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
        #if not token:
            return json_response(status_=401 ,message=invalid_msg)

        try:
            #secrets['JWT']
            token = auth_headers[1]
            logger.debug("Got token")
            data = jwt.decode(token,  secret , algorithms=["HS256"])
            logger.debug('DECODED DATA FROM TOKEN_REQ.PY ', data)
            #set global jwt_data
            g.jwt_data = data
            return f( *args, **kwargs)
        except jwt.ExpiredSignatureError:
             print('TOKEN INVALID : ', token)
             return json_response(status_=401 ,message=expired_msg) # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            logger.debug(e, 'TOKEN ERROR!!')
            return json_response(status_=401 ,message=expired_msg)

    return _verify

