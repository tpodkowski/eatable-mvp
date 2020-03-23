from flask import Blueprint, render_template, request, redirect
from app.models.models import Product, db

products_bp = Blueprint('products_bp', __name__,
                        template_folder='templates',
                        static_folder='static', static_url_path='assets')


@products_bp.route('/', methods=['GET'])
def get_products():
  products = Product.query.all()
  return render_template("products/list.html", products=products)


@products_bp.route('/', methods=['POST'])
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


@products_bp.route('/<int:id>', methods=['POST'])
def remove_product(id):
  product = Product.query.filter_by(product_id=id).first()
  db.session.delete(product)
  db.session.commit()
  return redirect("/products")
