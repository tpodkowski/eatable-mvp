from . import db

class Product(db.Model):
  __tablename__ = 'products'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), index=True, unique=True, nullable=False)
  calories = db.Column(db.Integer, index=False, unique=True, nullable=False)
  protein = db.Column(db.Float, index=False, unique=True, nullable=False)
  carbohydrates	= db.Column(db.Float, index=False, unique=True, nullable=False)
  fat	= db.Column(db.Float, index=False, unique=True, nullable=False)

  def __repr__(self):
    return '<Name %r>' % self.name
  
