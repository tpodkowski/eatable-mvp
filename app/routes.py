from flask import current_app as app
from flask import jsonify, redirect, render_template, request

from .models import Product, Recipe, db


@app.route('/', methods=['GET'])
def entry():
  products = Product.query.all()
  recipes = Recipe.query.all()
  return render_template("index.html", products=products, recipes=recipes, title="Eatable", template="body-background")

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
  return redirect("/products")


@app.route('/products/<int:id>', methods=['POST'])
def remove_product(id):
  product = Product.query.filter_by(id=id).first()
  db.session.delete(product)
  db.session.commit()
  return redirect("/products")


@app.route('/recipes', methods=['GET'])
def get_recipes():
  products = Product.query.all()
  recipes = Recipe.query.join(Recipe.products)
  return render_template("./recipes/recipes.html", recipes=recipes, products=products, title="Eatable - Produkty")


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

  return redirect("/recipes")


@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
  products = Product.query.all()
  recipe = Recipe.query.get(id)
  if recipe is not None:
    return render_template("./recipes/recipe.html", recipe=recipe, products=products, title="Eatable - {{  }}")
  else:
    return redirect('/recipes')


@app.route('/ingredients', methods=['GET', 'POST'])
def get_recipes_by_ingredients():
  products = Product.query.all()
  recipes = []

  if request.method == 'POST':
    product_ids = request.form.getlist('products')
    recipes = Recipe.query.filter(Recipe.products.any(Product.id.in_(product_ids))).all()
  else:
    products = Product.query.all()

  return render_template('./ingredients/ingredients.html', products=products, recipes=recipes, title="Eatable - Moja Lodówka")