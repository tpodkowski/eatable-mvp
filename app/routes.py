from flask import request, render_template
from flask import current_app as app, jsonify
from .models import db, Product


@app.route('/', methods=['GET'])
def entry():
  products = list(Product.query.all())
  return render_template("products.html", products=products, title="Show Products")


@app.route('/products', methods=['GET'])
def get_products():
  products = list(Product.query.all())
  return render_template("products.html", products=products, title="Show Products")

@app.route('/products', methods=['POST'])
def add_product():
  form = request.form
  print('DUPA')
  product = Product(
    name=form['name'],
    calories=form['calories'],
    protein=form['protein'],
    carbohydrates=form['carbohydrates'],
    fat=form['fat']
  )
  db.session.add(product)
  db.session.commit()
  
  products = Product.query.all()
  return render_template("products.html", products=products, title="Show Products")
