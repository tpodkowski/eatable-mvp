from app import db
from sqlalchemy.dialects import postgresql

recipes_products = db.Table(
  'recipes_products',
  db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.recipe_id')),
  db.Column('product_id', db.Integer, db.ForeignKey('product.product_id'))
)


class Recipe(db.Model):
  recipe_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  description = db.Column(postgresql.JSON)
  image_url = db.Column(db.String())
  url = db.Column(db.String())
  products = db.relationship('Product', secondary=recipes_products, backref=db.backref('recipes', lazy=True))


class Product(db.Model):
  product_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  calories = db.Column(db.Integer)
  protein = db.Column(db.Float)
  carbohydrates = db.Column(db.Float)
  fat = db.Column(db.Float)
# recipes = db.relationship('Recipe', secondary=recipes_products, backref=db.backref('products', lazy=True))
