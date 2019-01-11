from config import db
        
class User(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(12), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(35), nullable=True)
    car_id = db.Column(db.String(8), nullable=False)
    avatar = db.Column(db.String(200), nullable=True)

    def __init__(self, id, username, password, phone, email, car_id, avatar):
        self.id = id
        self.username = username
        self.password = password
        self.phone = phone
        self.email = email
        self.car_id = car_id
        self.avatar = avatar
        
    def __repr__(self):
        return '<User %r>' % self.username

    