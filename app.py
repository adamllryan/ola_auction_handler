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
from threading import Thread, Event
app = Flask(__name__, static_url_path='', static_folder='frontend/build')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)  # comment this on deployment
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

# DB Handling

class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]
    
# @dataclass
# class Auction(db.Model):
#     id: int = db.Column(db.Integer, primary_key=True)
#     name: str = db.Column(db.Text, nullable=False)
#     url: str = db.Column(db.Text, nullable=False)
#     src: str = db.Column(db.Text, nullable=True)
#     created_at: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())

#     def __repr__(self):
#         return f'<Auction {self.name}>'

@dataclass
class Item(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    auction: str = db.Column(db.Text, nullable=False)
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


# with app.app_context():
#     db.create_all()
#     db.session.commit()
# db.session.add_all(sample_auctions)
# db.session.commit()

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

scraper: SeleniumScraper
with app.app_context():
    items = set(map(lambda x: x.name, Item.query.all()))
    scraper = SeleniumScraper(items, True)
scraper.start()

def callback():
    while True:
        scraper.callback.wait()
        with app.app_context():
            items = scraper.export_()
            print("cleaning out old db items")
            db.session.execute(text("DELETE FROM item WHERE ends_at"))
            print(f"Writing {len(items)} items to db")
            #db.session.add_all(map(lambda x: Item(auction=x[0], name=x[1], url=x[2], src=x[3], last_price=x[4], retail_price=x[5], condition=x[6], ends_at=x[7]), items))
            for x in items:
                i = Item(auction=x[0], name=x[1], url=x[2], src=x[3], last_price=x[4], retail_price=x[5], condition=x[6], ends_at=x[7])
                # print(i, i.name, i.last_price, i.retail_price)
                db.session.add(i)
            # db.create_all()
                db.session.commit()
                scraper.callback.clear()
                scraper.logged_auctions = set(list(map(lambda x: x.name, Item.query.all())))
cbFunc = Thread(target=callback)
cbFunc.start()

@app.route('/flask/api/refresh')
def refresh():
    if not scraper.reload_called.is_set():
        scraper.reload_called.set()
        return jsonify('Refreshing!')
    else:
        return jsonify(scraper.get_progress())
    



