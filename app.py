from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from models.product import Product
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

load_dotenv()

app = Flask(__name__)

db = create_engine(os.getenv("DATABASE_URL"), echo=True)
base = declarative_base()

Session = sessionmaker(db)
session = Session()

doctor_strange = Product(name = "Carrot", calories = 41)
session.add(doctor_strange)
session.commit()

base.metadata.create_all(db)

@app.route("/")
def hello():
  return "Welcome to EATBALE API"


@app.route("/products")
def get_products():
  products = session.query(Product)
  result = []

  print(products)
  
  for product in products:
    result.append(product.name)
  
  return jsonify(result)


# @app.route("/name/<name>")
# def get_book_name(name):
#     return "name : {}".format(name)


# @app.route("/details")
# def get_book_details():
#     author = request.args.get('author')
#     published = request.args.get('published')
#     return "Author : {}, Published: {}".format(author, published)


if __name__ == '__main__':
  app.run()
