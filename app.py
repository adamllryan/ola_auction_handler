import datetime
import os.path
from dataclasses import dataclass
from flask import Flask, send_from_directory, jsonify
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS  # comment this on deployment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.inspection import inspect


from api.ApiHandler import HelloApiHandler

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app)  # comment this on deployment
api = Api(app)

# DB Handling

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]
    
@dataclass
class Auction(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.Text, nullable=False)
    url: str = db.Column(db.Text, nullable=False)
    src: str = db.Column(db.Text, nullable=True)
    created_at: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Auction {self.name}>'

@dataclass
class Item(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.Text, nullable=False)
    url: str = db.Column(db.Text, nullable=False)
    src: str = db.Column(db.Text, nullable=True)
    last_price: float = db.Column(db.Float, nullable=False)
    retail_price: float = db.Column(db.Float, nullable=False)
    condition: str = db.Column(db.Text, nullable=False)
    ends_at: datetime =  db.Column(db.DateTime(timezone=True))
    created_at: datetime =  db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f'<Item {self.name}>'


# 

@app.route("/", defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/flask/api/auction/<str:query>")
def get_auction(self, query):
    # & will separate each param by key and values
    query = query.replace('+', ' ')
    terms = query.split('&')
    # = will split key from values
    params = {}
    for term in terms:
        key, pair = term.split('=')
        params[key] = list(pair.split('%'))
    results = db.session.execute('SELECT * FROM mytable \
        WHERE column1 LIKE '{0}'')

class ApiHandler(Resource):
    def get(self):
        # get json data
        auctions = Auction.query.all()
        return jsonify(auctions)

    def post(self):
        # update

        return {
            'resultStatus': 'SUCCESS',
            'message': f"You posted {0} items :)"
        }


api.add_resource(ApiHandler, '/flask/api')

if __name__ == '__app__':
    sample_auctions = []
    for i in range(1,10):
        sample_auctions.append(Auction(name="Stow", url="google.comlol", src="nowhere"))
    db.create_all()
    db.session.add_all(sample_auctions)
    db.session.commit()