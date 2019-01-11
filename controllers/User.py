import sys
sys.path.append("..")
from models import User
import hashlib
import werkzeug
from flask_restful import reqparse, Resource
from config import db, ma

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class UserController(Resource):
    def __init__(self):
        self.args = ['username', 'password', 'phone', 'email', 'car_id', 'avatar']
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, help='missed username')
        self.parser.add_argument('password', type=str, required=True, help='missed password')
        self.parser.add_argument('phone', type=str, required=True, help='missed phone')
        self.parser.add_argument('email', type=str)
        self.parser.add_argument('car_id', type=str)
        self.parser.add_argument('avatar', type=werkzeug.datastructures.FileStorage, location='files')

    # 增
    def post(self):
        args = self.parser.parse_args()
        username = args['username']
        password = hashlib.md5(args['password'].encode()).hexdigest()
        phone = args['phone']
        avatar = args.get('avatar', None)
        email = args.get('email', None)
        _id = hashlib.md5(username.encode()).hexdigest()
        if User.query.get(_id):
            return {'message': 'already exist'}, 409
        car_id = args['car_id']
        user = User(_id, username, password, phone, email, car_id, avatar)
        db.session.add(user)
        db.session.commit()
        if avatar:
            avatar.save('avatar_{}.jpg'.format(username))
        return {'message': 'success'}, 201

    # 删
    def delete(self, id=None):
        if not id:
            return {'message': 'missed id'}
        user = User.query.get(id)
        if not user:
            return {'message': 'not exist'}, 404
        parser = reqparse.RequestParser()
        db.session.delete(user)
        db.session.commit()
        return {'message': 'success'}

    # 改
    def put(self, id=None):
        if not id:
            return {'message': 'missed id'}
        user = User.query.get(id)
        if not user:
            return {'message': 'not exist'}, 404
        parser = reqparse.RequestParser()
        for arg in self.args:
            parser.add_argument(arg, type=str)
        args = parser.parse_args()
        if hashlib.md5(args['password'].encode()).hexdigest() != user.password:
            return {'message': 'wrong password'}, 401
        for arg in args:
            if args[arg] and getattr(user, arg) != args[arg] and arg != 'username' and arg != 'password':
                setattr(user, arg, args[arg])
        db.session.add(user)
        db.session.commit()
        return {'message': 'success'}

    # 查
    def get(self, id=None):
        user_schema = UserSchema()
        if id:
            user = User.query.get(id)
            if not user:
                return {'message': 'not exist'}, 404
            return user_schema.dump(user).data
        users = []
        _users = User.query.all()
        for user in _users:
            users.append(user_schema.dump(user).data)
        return {
            'message': 'success',
            'total': len(_users), 
            'data': users
        }