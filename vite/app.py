import datetime
import os.path
from dataclasses import dataclass
import time
from flask import Flask, send_from_directory, jsonify, request, render_template
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS  # comment this on deployment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, text
from sqlalchemy.inspection import inspect
from flask_marshmallow import Marshmallow
from SeleniumScraper import SeleniumScraper
from threading import Thread
from sqlalchemy import exists, insert, select, update, delete
from json import dumps
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_url_path='', static_folder='frontend/build')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}

CORS(app)  # comment this on deployment
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# DB Handling

@dataclass
class Item(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    auction: str = db.Column(db.Text, nullable=False)
    owner_id: int = db.Column(db.Integer, nullable=True)
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
        fields = ('id', 'auction', 'owner_id', 'name', 'url', 'src', 'last_price', 'retail_price', 'condition', 'ends_at', 'created_at')

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

@dataclass
class Users(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.Text, nullable=False, unique=True)
    password: str = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'password')

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

scraper: SeleniumScraper
with app.app_context():
    items = db.session.query(Item.auction).distinct().all()
    scraper = SeleniumScraper(list(items), {
        'verbose': True,
        'demo': False,
        'show_display': True
    })
scraper.start()

def callback():
    while True:
        scraper.callback['page_refresh_callback'].wait()
        with app.app_context():
            items = scraper.export_()
            print(f"cleaning out old db items")
            db.session.execute(text("DELETE FROM item WHERE ends_at < date('now')"))
            print(f"Writing {len(items)} items to db")
            for x in items:
                i = Item(auction=x[0], name=x[1], url=x[2], src=x[3], last_price=x[4], retail_price=x[5], condition=x[6], ends_at=x[7])
                db.session.add(i)
            Item.query.filter(Item.ends_at<func.now()).delete()
            db.session.commit()
            auctions = db.session.query(Item.auction).distinct().all()
            print(auctions)
            scraper.auction_data['logged_auctions'] = auctions
            scraper.callback['page_refresh_callback'].clear()
cbFunc = Thread(target=callback)
cbFunc.start()

@app.route("/api/v1/search/<Query>")
def get_items(Query):
    results = []
    print(Query)
    [Query, page] = Query.split('&_pgn=')
    page = int(page)
    if Query=='':
        return jsonify(items_schema.dump(db.session.execute(text("SELECT * FROM item WHERE ends_at > date('now') LIMIT 50 OFFSET " + str(page*50))).fetchall()))
    # replace + with space because no space in url
    Query = Query.replace('+', ' ')
    # & separates query parameters
    terms = Query.split('&')
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
        query = []
        for value in params[key]:
            query.append(f"{key} LIKE '%{value}%'")
        queries.append(" OR ".join(query))
    search += "(" + ") AND (".join(queries) + ")"
    if 'owner_id' not in queries:
        search += ' AND (ends_at > date(\'now\'))'
    
    search += 'LIMIT 50 OFFSET ' + str(page*50)
    print(search)
    # TODO: return set(results)
    final = items_schema.dump(db.session.execute(text(search)).fetchall())
    return jsonify(final)

@app.route('/api/v1/refresh',methods = ['POST'])
def refresh():
    if request.method == 'POST':
        if not scraper.callback['page_refresh_trigger'].is_set():
            auctions = db.session.query(Item.auction).distinct().all()
            #print(auctions)
            scraper.logged_auctions = auctions
            scraper.callback['page_refresh_trigger'].set()
        return jsonify(scraper.get_progress())

@app.route('/api/v1/refresh/progress', methods = ['GET'])
def refresh_progress():
    if request.method == 'GET':
        return jsonify(scraper.get_progress())

@app.route('/api/v1/owner/<int:item_id>/<owner>', methods = ['GET', 'POST'])
def owner(item_id, owner):
    if request.method == 'POST':
        # check owner exists
        query = db.session.execute(select(Users.id).where(Users.name==owner)).fetchall()
        if len(query)==1:
            print(query[0][0], item_id)
            db.session.execute(update(Item).where(Item.id==int(item_id)).values(owner_id=query[0][0]))
            db.session.commit()
            #db.session.execute(text(f"UPDATE item SET owner_id = {query[0][0]} WHERE id = '{id}'"))
            return jsonify('SUCCESS')
        else:
            return jsonify('FAILURE')
@app.route('/api/v1/owner/<int:item_id>', methods = ['GET'])
def get_owner(item_id):
    if request.method == 'GET':
        query = db.session.execute(select(Item.owner_id).where(Item.id==item_id)).fetchall()
        if len(query)==1:
            name = db.session.execute(select(Users.name).where(Users.id==query[0][0])).fetchall()
            if len(name)==1:
                return jsonify(name[0][0])
            else:
                return jsonify('Invalid Owner')
        else:
            return jsonify('No Owner')

@app.route('/api/v1/u/<username>', methods = ['GET', 'POST'])
def user(username):
    query = db.session.execute(select(Users.id).where(Users.name==username)).fetchall()
    if request.method == 'POST':
        if len(query)==0:
            db.session.execute(insert(Users).values(name=username, password='NULL'))
            db.session.commit()
            return jsonify('SUCCESS')
        else:
            return jsonify('FAILURE')
    elif request.method == 'GET':
        if len(query)==1:
            return jsonify(query[0][0])
        else:
            return jsonify('FAILURE')

# @socketio.on('/api/v1/websocket')
# def socket():
#     emit('after connect', {'data': 'test'})
@socketio.on('socket')
def socket(data):
    emit('receive', 'test')

@socketio.on('refresh_page')
def refresh_call():
    if scraper.callback['page_refresh_trigger'].is_set():
        emit('err', 'Scraper is running or on cooldown')
    else:
        auctions = db.session.query(Item.auction).distinct().all()
        scraper.logged_auctions = auctions
        scraper.callback['page_refresh_trigger'].set()
        while not scraper.callback['page_refresh_callback'].is_set():
            time.sleep(1)
            emit('refresh_progress', jsonify(scraper.get_progress().progress))
        emit('refresh_progress', 'completed')
        