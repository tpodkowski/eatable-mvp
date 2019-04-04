from flask import current_app as app
from flask import jsonify, redirect, render_template, request

from .models import Product, Recipe, db


@app.route('/', methods=['GET'])
def entry():
  products = Product.query.all()
  recipes = Recipe.query.all()
  return render_template("index.html", products=products, recipes=recipes)

@app.route('/products', methods=['GET'])
def get_products():
  products = Product.query.all()
  return render_template("./products/products.html", products=products)

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
  
  return redirect("/")

@app.route('/products/<int:id>', methods=['POST'])
def remove_product(id):
  product = Product.query.filter_by(id=id).first()
  db.session.delete(product)
  db.session.commit()
  return redirect("/")


@app.route('/recipes', methods=['GET'])
def get_recipes():
  recipes = Recipe.query.all()
  products = Product.query.all()
  return render_template("./recipes/recipes.html", recipes=recipes, products=products, title="Show recipes")

@app.route('/recipes', methods=['POST'])
def add_recipe():
  product_ids = request.form.getlist('products')
  products = list(map(lambda id: Product.query.get(id), product_ids))

  recipe = Recipe(
    name = request.form['name'],
    description = request.form['description'],
    products = products
  )

  db.session.add(recipe)
  db.session.commit()

  return redirect("/")
