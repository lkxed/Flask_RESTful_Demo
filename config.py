# -*- encoding: utf8 -*-
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
import pymysql

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@server/PMS'

db = SQLAlchemy(app)

ma = Marshmallow(app)

api = Api(app)
