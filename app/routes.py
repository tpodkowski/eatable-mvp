from flask import request, render_template, redirect
from flask import current_app as app, jsonify
from .models import db, Product


@app.route('/', methods=['GET'])
def entry():
  products = Product.query.all()
  return render_template("products.html", products=products, title="Show Products")

@app.route('/products', methods=['POST'])
def add_product():
  product = Product(
    name=request.form['name'],
    calories=request.form['calories'],
    protein=request.form['protein'],
    carbohydrates=request.form['carbohydrates'],
    fat=request.form['fat']
  )
  db.session.add(product)
  db.session.commit()
  
  products = Product.query.all()
  return redirect("/")

@app.route('/products/<int:id>', methods=['POST'])
def remove_product(id):
  product = Product.query.filter_by(id=id).first()
  db.session.delete(product)
  db.session.commit()
  return redirect("/")
