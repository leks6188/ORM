import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

login_db = 'postgres'
password_db = 'postgres'
name_db = ''

DSN = f'postgresql://{login_db}:{password_db}@localhost:5432/{name_db}'
engine = sqlalchemy.create_engine(DSN)

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
    name = sqlalchemy.Column(sqlalchemy.String(60) ,nullable=False)
    books = relationship('Book', back_populates='publisher')

class Book(Base):
    __tablename__ = 'book'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(60), nullable=False)
    id_publisher = sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.ForeignKey('publisher.id'), nullable=False)
    publisher = relationship('Publisher', back_populates='books')
    stocks = relationship('Stock', back_populates='book')


class Shop(Base):
    __tablename__ = 'shop'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key= True)
    name = sqlalchemy.Column(sqlalchemy.String(60), nullable=False)
    stocks = relationship('Stock',back_populates='shop')


class Stock(Base):
    __tablename__ = 'stock'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_book = sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.ForeignKey('book.id'), nullable=False)
    id_shop = sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.ForeignKey('shop.id'), nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer)

    book = relationship('Book', back_populates='stocks')
    shop = relationship('Shop', back_populates='stocks')
    sales = relationship('Sale', back_populates='stock')

class Sale(Base):
    __tablename__ = 'sale'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    price = sqlalchemy.Column(sqlalchemy.DECIMAL, nullable=False)
    date_sale = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    id_stock = sqlalchemy.Column(sqlalchemy.Integer,ForeignKey('stock.id'))
    count = sqlalchemy.Column(sqlalchemy.Integer)

    stock = relationship('Stock', back_populates='sales')
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

new_publisher = [Publisher(name = 'Бродский'), Publisher(name = 'Лавкрафт'), Publisher(name = 'Мартин')]
books = [Book(title = "Часть Речи",id_publisher=1), Book(title='Тень над Иннсмутом', id_publisher=2),
         Book(title= "Чистый код",id_publisher = 3)]
shops = [Shop(name='Буквоед'), Shop(name='Книжный дом'), Shop(name='Лабиринт')]
stock = [Stock(id_book=1,id_shop=1,count=3),
         Stock(id_book=1,id_shop=2,count = 3),
         Stock(id_book=1,id_shop=3,count = 3)]

sale = [Sale(price=10, date_sale='2025-03-07', id_stock=2, count = 2),
        Sale(price=20, date_sale='2025-03-09', id_stock=1, count = 1)]

session.add_all(new_publisher + books + shops + stock + sale)
session.commit()

name_publisher = "Бродский"
Books = (session.query(Book).join(Publisher).join(Stock).join(Shop).join(Sale)
         .filter(Publisher.name == name_publisher).all())
for book in Books:
    for stock in book.stocks:
        for sale in stock.sales:
            print(f"""Название книги:{book.title}, Магазин:{stock.shop.name},
                  Цена:{sale.price}, Дата: {sale.date_sale}""")
session.close()            