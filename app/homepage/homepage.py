from flask import Blueprint, render_template, request
from app.models.models import Product, Recipe

homepage_bp = Blueprint('homepage_bp', __name__,
                             template_folder='templates',
                             static_folder='static', static_url_path='assets')

@homepage_bp.route('/', methods=['GET'])
def entry():
  products = Product.query.all()
  recipes = Recipe.query.all()
  return render_template("homepage/index.html", products=products, recipes=recipes, title="Eatable", template="body-background")