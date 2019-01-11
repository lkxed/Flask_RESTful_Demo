import sys
sys.path.append("..")
import random
from flask_restful import reqparse, Resource

users = []

codes = []

source = [str(n) for n in range(10)]

def getCode():
    code = ''.join(random.sample(source, 6))
    return code

def validate(phone, code):
    for one in codes: 
        if one['phone'] == phone and one['code'] == code:
            return True
    return False

def does_phone_exist(phone):
    for user in users:
        if phone == user['phone']:
            return True
    return False
    
class RegisterController(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('phone', type=str, required=True, help='missed phone')

    def get(self, phone, code):
        if not does_phone_exist(phone):
            return {'message': 'not exist'}, 404
        elif not validate(phone, code):
            return {'message': 'wrong code'}
        else:
            return {'message': 'success'}

    def post(self):
        args = self.parser.parse_args()
        code = {'phone': args['phone'], 'code': getCode()}
        codes.append(code)
        users.append({'phone': args['phone']})
        return {
            'message': 'success',
            'data': code
        }, 201
