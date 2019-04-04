from . import db

products = db.Table('products',
  db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
  db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class Recipe(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), index=True, unique=False, nullable=False)
  description = db.Column(db.String(), index=True, unique=False, nullable=False)
  products = db.relationship('Product', secondary=products, lazy='subquery', backref=db.backref('recipes', lazy=True))

class Product(db.Model): 
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), index=True, unique=False, nullable=False)
  calories = db.Column(db.Integer, nullable=False)
  protein = db.Column(db.Float, nullable=False)
  carbohydrates	= db.Column(db.Float, nullable=False)
  fat	= db.Column(db.Float, nullable=False)