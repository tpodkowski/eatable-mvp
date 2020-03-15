from . import db
from sqlalchemy.dialects import postgresql

recipes_to_products_table = db.Table('recipes_to_products',
  db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
  db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)

class Recipe(db.Model):
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(postgresql.JSON)
    image_url = db.Column(db.String())
    url = db.Column(db.String())
    products = db.relationship('Product', secondary=recipes_to_products_table, back_populates="recipes")
    def __repr__(self):
            return repr(self.name)

class Product(db.Model): 
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  calories = db.Column(db.Integer)
  protein = db.Column(db.Float)
  carbohydrates	= db.Column(db.Float)
  fat	= db.Column(db.Float)
  recipes = db.relationship('Recipe', secondary=recipes_to_products_table, back_populates="products") 
  def __repr__(self):
    return repr(self.name)
