from flask import Blueprint, render_template, request, redirect
from app.models.models import Recipe, Product


my_fridge_bp = Blueprint('my_fridge_bp', __name__,
                        template_folder='templates',
                        static_folder='static', static_url_path='assets')


@my_fridge_bp.route('/', methods=['GET', 'POST'])
def get_recipes_by_ingredients():
  products = Product.query.all()
  recipes = []

  if request.method == 'POST':
    product_ids = request.form.getlist('products')
    recipes = Recipe.query.filter(Recipe.products.any(Product.product_id.in_(product_ids))).all()
  else:
    products = Product.query.all()

  return render_template('ingredients/ingredients.html', products=products, recipes=recipes, title="Eatable - Moja Lodówka")
