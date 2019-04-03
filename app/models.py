from . import db

class Product(db.Model):
  __tablename__ = 'products'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), index=True, unique=False, nullable=False)
  calories = db.Column(db.Integer, nullable=False)
  protein = db.Column(db.Float, nullable=False)
  carbohydrates	= db.Column(db.Float, nullable=False)
  fat	= db.Column(db.Float, nullable=False)
  recipes = db.relationship('Recipe', lazy=True)


class Recipe(db.Model):
  __tablename__ = 'recipes'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), index=True, unique=False, nullable=False)
  description = db.Column(db.String(), index=True, unique=False, nullable=False)
  products = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  
