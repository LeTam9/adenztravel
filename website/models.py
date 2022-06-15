from datetime import datetime
from email.policy import default
from itertools import product
from unicodedata import name
import pymysql
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

CONNECTION_STRING = "mongodb+srv://tamle6099:Thinh123@cluster0.103e4.mongodb.net/Cluster0?retryWrites=true&w=majority"
CONNECTION_STRING_MYSQL = "mysql+pymysql://root:1@localhost/adenz"

class Database:
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def connectMYSQL(self):
        conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "1",
        db='adenz',
        )

        return conn

    def connectSQLAlchemy(self):
        engine = create_engine(CONNECTION_STRING_MYSQL).execution_options(isolation_level="AUTOCOMMIT")
        return engine.raw_connection()
        
database =  Database('localhost', 'root', '1', 'adenz')
db = database.connectSQLAlchemy()
Base = declarative_base()


class BaseModel():
    __abastract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class TourTravel(BaseModel):
    __tablename__ = "tourtravel"
    name = Column(String(100), nullable=True)
    products = relationship('Products', backref='tourtravel', lazy=True)

    def __str__(self):
        return self.name

class Products(BaseModel):
    __tablename__ = "products"
    print(product)
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(500), nullable=False )
    image = Column(String(255))
    time = Column(String(255))
    departure = Column(Float)
    price = Column(Float, default=0)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    created_id = Column(Integer, ForeignKey(TourTravel.id), nullable=False)

    def __repr__(self):
        return "<Products(name='%s' image='%s', time='%s', departure='%s',price='%s',active='%s', create_date='%s', created_id='%s')>" % (
        self.name,self.image, self.time, self.departure,self.price,self.active, self.created_date, self.created_id)


Session = sessionmaker(db)
session = Session()
def read_json(path):
    f = open(path, "r")
    data = json.load(f)
    f.close()
    return data

def load_toutravel():
    return read_json('website/data/tourtravel.json')

def load_products():
    products =  read_json('website/data/products.json')
    return products 
    
def save_product_json():
    products =  read_json('website/data/products.json')
    for product in products:
        save_product_to_db(product=product)


def save_product_to_db(product):
    name = product["name"]
    image = product["image"]
    time = product["time"]
    departure = product["departure"]
    price = product["price"]
    cursor = db.cursor()

    sqlStatement = 'insert into products (name, price, image,departure, active, create_date) values (%s, %s, %s, %s, %s,%s)'
    sqlValues = (name, price, image,time,departure, True, datetime.now())
    cursor.execute(sqlStatement, sqlValues)
    db.commit()


    cursor.execute('select * from products')
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)
  
    return "add successful data"


def get_product_by_id(product_id):
    products =  read_json('website/data/products.json')
    for p in products:
        if p ['id'] == product_id:
            return p
    