from database.db import db
from flask_bcrypt import generate_password_hash, check_password_hash


class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    username = db.fields.StringField(required=True, unique=True)
    name = db.fields.StringField(required=True)
    password = db.fields.StringField(required=True, min_length=7)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

