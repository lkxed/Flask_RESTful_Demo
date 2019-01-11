from controllers.User import UserController
from controllers.Login import LoginController
from controllers.Register import RegisterController
from config import api

api.add_resource(RegisterController, '/register', '/register/<string:phone>/<string:code>')
api.add_resource(UserController, '/users', '/users/<string:id>')
api.add_resource(LoginController, '/login')