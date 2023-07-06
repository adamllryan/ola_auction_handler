import os.path

from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS  # comment this on deployment
from flask_sqlalchemy import SQLAlchemy


from api.ApiHandler import HelloApiHandler

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app)  # comment this on deployment
api = Api(app)

# DB Handling

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route("/", defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')


class ApiHandler(Resource):
    def get(self):
        # get json data

        return {
            'resultStatus': 'SUCCESS',
            'message': "You got :)"
        }

    def post(self):
        # update

        return {
            'resultStatus': 'SUCCESS',
            'message': "You posted :)"
        }


api.add_resource(ApiHandler, '/flask/api')
