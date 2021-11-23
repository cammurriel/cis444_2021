from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Get Books Handle Request")
    cur = g.db.cursor()
    cur.execute("select * from books")
    books = []
    for r in cur.fetchall():
        print('BOOKS DATA: ',r)
        book_dict = {"book_id": r[0], "book_title":r[1], "book_price":r[2]}
        books.append(book_dict)
        '''    cur.execute("create table music ( song_name varchar(255), rating int);")
    db.commit()'''


    return json_response( token = create_token(  g.jwt_data ) , books = books)

