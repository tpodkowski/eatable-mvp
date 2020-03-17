from flask import Blueprint, render_template, request, redirect
from app.models.models import Product, Recipe, db

recipes_bp = Blueprint('recipes_bp', __name__,
                        template_folder='templates',
                        static_folder='static', static_url_path='assets')

@recipes_bp.route('/', methods=['GET'])
def get_recipes():
  products = Product.query.all()
  recipes = Recipe.query.join(Recipe.products)
  return render_template("recipes/recipes.html", recipes=recipes, products=products, title="Eatable - Produkty")


@recipes_bp.route('/', methods=['POST'])
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


@recipes_bp.route('/<int:id>', methods=['GET'])
def get_recipe(id):
  products = Product.query.all()
  recipe = Recipe.query.get(id)

  if recipe is not None:
    title = "Eatable - " + recipe.name
    return render_template("recipes/recipe.html", recipe=recipe, products=products, title=title)
  else:
    return redirect('/recipes')
