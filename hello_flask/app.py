from flask import Flask,render_template,request, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import datetime
import bcrypt


from db_con import get_db_instance, get_db

app = Flask(__name__ , template_folder = "templates")
FlaskJSON(app)

USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"
JWT_SECRET = None

global_db_con = get_db()


with open("secret", "r") as f:
    JWT_SECRET = f.read()

@app.route('/caprice') #endpoint
def index():
    return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']

@app.route('/buy') #endpoint
def buy():
    return 'Buy'

@app.route('/hello') #endpoint
def hello():
    return render_template('hello.html',img_url=IMGS_URL[CUR_ENV] ) 

@app.route('/back',  methods=['GET']) #endpoint
def back():
    return render_template('backatu.html',input_from_browser=request.args.get('usay', default = "nothing", type = str) )

@app.route('/backp',  methods=['POST']) #endpoint
def backp():
    print(request.form)
    salted = bcrypt.hashpw( bytes(request.form['fname'],  'utf-8' ) , bcrypt.gensalt(10))
    print(salted)

    print(  bcrypt.checkpw(  bytes(request.form['fname'],  'utf-8' )  , salted ))

    return render_template('backatu.html',input_from_browser= str(request.form) )

@app.route('/auth',  methods=['POST']) #endpoint
def auth():
        print(request.form)
        return json_response(data=request.form)



#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    return render_template('A2_CamMurriel.html', server_time= str(datetime.datetime.now()) )

@app.route('/getTime') #endpoint
def get_time():
    return json_response(data={"password" : request.args.get('password'),
                                "class" : "cis44",
                                "serverTime":str(datetime.datetime.now())
                           }
                )

@app.route('/auth2') #endpoint
def auth2():
    jwt_str = jwt.encode({"username" : "cary",
                            "age" : "so young",
                            "books_ordered" : ['f', 'e'] } 
                            , JWT_SECRET, algorithm="HS256")
    print(request.form['username'])
    return json_response(jwt=jwt_str)

@app.route('/exposejwt') #endpoint
def exposejwt():
    jwt_token = request.args.get('jwt')
    print(jwt_token)
    return json_response(output=jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"]))


@app.route('/hellodb') #endpoint
def hellodb():
    cur = global_db_con.cursor()
    cur.execute("insert into books values( 0, 100);")
    global_db_con.commit()
    return json_response(status="good")

#Assignment #3
@app.route('/', methods=['GET'])
def loginPage():
    return render_template('Books2.html')


@app.route('/login', methods=['POST']) #endpoint
def authUser():
    global token
    print('here ',request.json)
    cur = global_db_con.cursor()
    user = request.form['username']
    passwrd = request.form['password']

    cur.execute(f"SELECT * FROM users WHERE username = '{user}';")

    #1. query the db                                                                                                                      
    print('1')
    #cur.execute("SELECT username FROM users WHERE id = 1")                                                                                
    print('2')
    #2 fetch one                                                                                                                          
    userRow = cur.fetchone()
    print(userRow)
    #3. if user row is none return jsonify invalid username check if fetch one is not none                                                
    if userRow is None:
        return jsonify({"message" : "INVALID INPUT", 'token' : None})
    #4. check the pw by bcrypt check password                                                                                              
    else:
         userPass = userRow[2]
         userPass = bytes(userPass,"utf-8")

         print (userPass, '', passwrd)
         isValid = bcrypt.checkpw(bytes(passwrd,('utf-8')),userPass)
          #5 if authenticated return a jwt token otherwise return error message                                                            
         if isValid:
             print('true')
             jwt_str = jwt.encode({"username" :"cam" }
                            , JWT_SECRET, algorithm="HS256")

             print('JWT: ',jwt_str)
             print(jsonify({'message' : 'VALID USER, TOKEN IS SENT', 'token' : jwt_str}))
             return jsonify({'message' : 'VALID USER, TOKEN IS SENT', 'token' : jwt_str})
         else:
             print('false')
    

   

      
app.run(host='0.0.0.0', port=80)
