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
