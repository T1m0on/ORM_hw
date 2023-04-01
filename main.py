import sqlalchemy
from sqlalchemy.orm import sessionmaker
from operator import or_
import os
import json
from models import *

DSN = 'postgresql://postgres:postgresA@localhost:5432/hw_5_sql'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

#create_tables(engine)
#export_data_from_json()


def export_data_from_json():
    with open(f'{os.path.join(os.getcwd(), "fixtures", "tests_data")}.json', "r") as file:
        data = json.load(file)
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


def get_shop_by_publisher(publisher_name):
    query = session.query(Publisher, Book, Stock, Shop).join(Stock.shop).join(Stock.book).join(
        Book.publisher).filter(Book.id_publisher == publisher_name)
    for model in query:
        print(model[3])


def get_sales(id=None, name=None):
    query = session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale).join(Publisher).join(
        Stock).join(Sale).join(Shop).filter(or_(Publisher.id == id, Publisher.name == name))

    for book, shop, price, count, date in query:
        print(f'{book} | {shop} | {price * count} | {date}')

#тесты
#get_shop_by_publisher('Pearson')
#get_sales(id=4)
#get_sales(name='Pearson')

session.close()
