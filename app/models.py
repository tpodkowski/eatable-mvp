from . import db

class Product(db.Model):
  __tablename__ = 'products'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), index=True, unique=False, nullable=False)
  calories = db.Column(db.Integer, index=False, unique=False, nullable=False)
  protein = db.Column(db.Float, index=False, unique=False, nullable=False)
  carbohydrates	= db.Column(db.Float, index=False, unique=False, nullable=False)
  fat	= db.Column(db.Float, index=False, unique=False, nullable=False)

  def __repr__(self):
    return '<Name %r>' % self.name
  
