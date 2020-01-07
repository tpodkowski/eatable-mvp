from urllib import request
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
def calculateBMI():
  text = "severely overweight"
  bmi = 0
  if request.method == 'POST':
    name = request.form['name']
    height = float(request.form.get("height"))/100
    weight = float(request.form.get("weight"))
    bmi = weight / pow(height, 2)
    if (bmi < 16):
      text = ("severely underweight")
    elif (bmi >= 16 and bmi < 18.5):
      text = ("underweight")
    elif (bmi >= 18.5 and bmi < 25):
      text = ("Healthy")
    elif (bmi >= 25 and bmi < 30):
      text = ("overweight")

    #data = request.form
  return render_template('./bmi/bmi.html', bmi=bmi, description=text)


@app.route('/bmr', methods=['GET', 'POST'])
def calculateBMR():
  if request.method == 'POST':
    name = request.form['name'],
    height = request.form['height'],
    weight = request.form['weight'],
    age = request.form['age'],
    sex = request.form['sex'],
    activity = request.form['activity']

    data = request.form
    '''
    height *= 100
    if gender == 'F' or gender == 'f':
        bmr = 655 + (4.35 * weight) + (4.7 * height) - (4.7 * age)
    elif gender == 'M' or gender == 'm':
        bmr = (10* weight) + (6.25*height) -(5*age) + 5
        bmr = bmr * 
    else:
        return "You gave wrong value, try again"
 
    https://www.thecalculatorsite.com/articles/health/bmr-formula.php
    '''
  return render_template('./bmr/bmr.html')