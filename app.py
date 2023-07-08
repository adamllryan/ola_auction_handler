import datetime
import os.path
from dataclasses import dataclass
from flask import Flask, send_from_directory, jsonify
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS  # comment this on deployment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, text
from sqlalchemy.inspection import inspect
from flask_marshmallow import Marshmallow
from SeleniumScraper import SeleniumScraper

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app)  # comment this on deployment
api = Api(app)


# DB Handling

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

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

class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'auction', 'name', 'url', 'src', 'last_price', 'retail_price', 'condition', 'ends_at', 'created_at')

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
# 

@app.route("/", defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/flask/api/items/<Query>")
def get_items(Query):
    print(Query)
    results = []
    # replace + with space because no space in url
    Query = Query.replace('+', ' ')
    print(Query)
    # & separates query parameters
    terms = Query.split('&')
    print(terms)
    # = will split key from values
    params = {}
    # split KP and then phrases by %
    for term in terms:
        key, pair = term.split('=')
        params[key] = pair.split('%')
        print(key, params[key])
    search = "SELECT * FROM item WHERE "
    queries = []
    for key in params:
        for value in params[key]:
            queries.append(f"{key} LIKE '%{value}%'")
    search += " OR ".join(queries)
    # TODO: return set(results)
    final = items_schema.dump(db.session.execute(text(search)).fetchall())
    return jsonify(final)
# names = db.session.execute(text("SELECT name FROM item")).fetchall()
scraper = SeleniumScraper([], False)
scraper.start()

@app.route('/flask/api/refresh')
def refresh():
    if not scraper.reload_called.is_set():
        scraper.reload_called.set()
        return jsonify('Refreshing!')
    else:
        return jsonify(scraper.get_progress())


if __name__ == '__app__':
    sample_auctions = []
    for i in range(1,10):
        sample_auctions.append(Auction(name="Stow", url="google.comlol", src="nowhere"))
    db.create_all()
    db.session.add_all(sample_auctions)
    db.session.commit()