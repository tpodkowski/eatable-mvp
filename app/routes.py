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
    image_url = request.form['image_url'],
    products = products
  )

  db.session.add(recipe)
  db.session.commit()

  return redirect("/recipes")


@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
  products = Product.query.all()
  recipe = Recipe.query.get(id)
  title = "Eatable - " + recipe.name
  
  if recipe is not None:
    return render_template("./recipes/recipe.html", recipe=recipe, products=products, title=title)
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

@app.route('/bmi', methods=['GET','POST'])
def calculate_bmi():
  bmi = None
  
  if request.method == 'POST':
    bmi = None
    height = float(request.form.get("height"))/100
    weight = float(request.form.get("weight"))
    bmi = weight / pow(height, 2)
    bmi = round(bmi, 2)

  return render_template('./bmi/bmi.html', bmi=bmi)


@app.route('/bmr', methods=['GET', 'POST'])
def calculate_bmr():
  bmr = 0.0
  activity = 1

  if request.method == 'POST':
    height = float(request.form.get('height'))
    weight = float(request.form.get('weight'))
    age = float(request.form.get('age'))
    sex = float(request.form.get('sex'))
    activity = float(request.form.get('activity'))

  #women
    if sex == 1:
      bmr = 655 + (9.563 * weight) + (1.85 * height) - (4.676 * age)
      bmr = bmr * activity
  #men
    else:
      bmr = 66.74 + (13.75 * weight) + (5.003 * height) - (6.755 * age) + 5
      bmr = bmr * activity

  bmr = round(bmr, 2)

  return render_template('./bmr/bmr.html', bmr=bmr, activity=activity)

@app.route('/bf', methods=['GET', 'POST'])
def calculate_bf():
  bf = 0.0

  if request.method == 'POST':
    sex = float(request.form.get('sex'))
    weight = float(request.form.get('weight'))
    waist = float(request.form.get('waist'))

    if sex == 1:
      d = (((4.15 * waist) / 2.54) - (0.082 * weight * 2.2)) - 76.76

    else:
      d = (((4.15 * waist) / 2.54) - (0.082 * weight * 2.2)) - 98.42

  bf = round(d / (weight*2.2) * 100, 2)

  return render_template('./bf/bf.html', bf=bf)