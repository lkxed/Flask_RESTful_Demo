import sys
sys.path.append('..')
from flask_restful import reqparse, Resource
from models import User
import hashlib

class LoginController(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('account', type=str, required=True, help='missed account')
        self.parser.add_argument('password', type=str, required=True, help='missed password')

    def post(self):
        args = self.parser.parse_args()
        account = args['account']
        password = args['password']
        user = User.query.filter_by(username=account).first()
        if not user:
            user = User.query.filter_by(phone=account).first()
        if not user:
            return {'message': 'not exist'}, 404
        if hashlib.md5(password.encode()).hexdigest() == user.password:
            return {'message': 'success'}
        else:
            return {'message': 'wrong password'}, 401