from flask import Flask, jsonify, request, redirect, url_for, session, json, request
from run import *
from datetime import datetime, date, timedelta, time
import datetime
import jwt as JWTT

import redis
import MySQLdb.cursors
import mysql.connector
from passlib.hash import pbkdf2_sha256 as sha256

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'


ACCESS_EXPIRES = timedelta(minutes=512655)   
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
jwt = JWTManager(app)
config={
    'host':'',
    'user' :'',
    'password' :'',
    'port':3306,
    'database':''
  
}




redis_host = 'localhost'
redis_port = 6379
r = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)




# merchant signin
@app.route('/api/merchant/signin', methods=['POST'])
async def merchant_signin():
    # global account_set
    try:
        data = request.json
        email = data['email']
        password = data['password']
        if not email:
            return jsonify(msg= "email can't be empty"),403
        if not password:
            return jsonify(msg= "password can't be empty"),403
        mydb = mysql.connector.connect(**config)
        my_cursor = mydb.cursor(buffered=True)
        sql = 'SELECT * FROM  merchant WHERE email =%s'
        datas = [email]
        my_cursor.execute(sql, datas)
        # my_cursor.execute('''SELECT * FROM  merchant WHERE email =%s''', [email])
        user = my_cursor.fetchone()
       
        if not user:
            my_cursor.close()
            mydb.close()
            return jsonify(msg="invalid login"),403
        else:
            
            if user and sha256.verify(password, user[8]):
                if user[10] == "1":
                    if user[5] and user[6] == 1:      
                        access_token = create_access_token(identity=user)
                        now = datetime.datetime.now()
                        myquery = 'SELECT  withdrawal_recipient_code FROM  merchant_account WHERE restaurant_id=%s'
                        mydata = [user[0]]
                        my_cursor.execute(myquery, mydata)
                        acc_num = my_cursor.fetchone()
                    
                        if not acc_num[0]:
                            account_set = False
                        
                        else:
                            account_set = True
                        
                        sqlQ = 'UPDATE merchant SET last_login=%s WHERE email= %s'
                        dataQ = [now, email]
                        my_cursor.execute(sqlQ, dataQ)
                        mydb.commit()
                        my_cursor.close()
                        mydb.close()
                        # data = {'access_token':access_token, 'name':user[2] 'email':user[3], 'phone_number':user[4],'about':user[5], 'image':user[7]}
                        return jsonify({'access_token':access_token, 'name':user[1], 'account_set':account_set, 'restaurant_id':user[0] }),200
                    else:
                            my_cursor.close()
                            mydb.close()
                            return jsonify(msg="your account is not active"),403
                else:    
                     
                    return jsonify(msg="Your email has not be verified, a link has been sent to your email"),403 
            else:
                my_cursor.close()
                mydb.close()
                return jsonify(msg="invalid login"),403                 
    except Exception as e:
           
        return jsonify(msg=e)     


@jwt_required() 
def account_status():
    current_user = get_jwt_identity()
    user_id = current_user[0]
    mydb = mysql.connector.connect(**config)
    my_cursor = mydb.cursor(buffered=True)
    my_cursor.execute('''SELECT account_status FROM  merchant WHERE restaurant_id =%s''', [user_id])
    user = my_cursor.fetchone()
   #  print(user)
    if user[0] == 0:
        return jsonify(msg= "your account has been suspended")
   

@app.before_request
def   is_not_blacklisted():
    authorization = request.headers.get('Authorization')

    if authorization:
      
         try:
            mydb = mysql.connector.connect(**config)
            my_cursor = mydb.cursor(buffered=True)
            status = account_status()
            if status :
                return jsonify(msg= "your account has been suspended")
            else:
               token = authorization.split(" ")[1] 
               decode = JWTT.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])

               jti = decode["jti"]
               my_cursor.execute('SELECT * FROM merchant_black_list WHERE jti=%s  ', [jti])
               query = my_cursor.fetchone()
               if query:
                  my_cursor.close()
                  mydb.close()
                  return jsonify(success= False, msg= "this is currently unavailable to you, login"),406
               
         except JWTT.ExpiredSignatureError:
            my_cursor.close()
            mydb.close()
            return jsonify("signature has expired"),401 
         except JWTT.InvalidTokenError:
            return jsonify("invalid token"),401
         except Exception as e:
            my_cursor.close()
            mydb.close()
            return jsonify(msg=e)  