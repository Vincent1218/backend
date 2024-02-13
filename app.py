from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from database.db import initialize_db
from flask_restful import Api
from resources.errors import errors
from resources.routes import initialize_routes

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_ALLOW_HEADERS'] = 'Content-Type'


# app.config.from_envvar('ENV_FILE_LOCATION')
# Use environment variables for configuration
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
app.config['MONGODB_SETTINGS'] = {
    'host': os.environ.get('MONGODB_HOST'),
}

print("Boom1", os.environ.get('MONGODB_HOST'))
print("Boom2", os.environ.get('JWT_SECRET_KEY'))


api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

initialize_db(app)
initialize_routes(api)

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
