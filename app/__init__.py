from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import random
import numpy as np

db = SQLAlchemy()

def create_app():
  app = Flask(__name__)
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  app.config["SQLALCHEMY_ECHO"] = True

  db.init_app(app)
  app.config.from_object('config.Config')
  
  with app.app_context():
    from . import routes
    from . import scrapper
    from . import models
    
    db.drop_all()
    db.create_all()    

    recipes = scrapper.fetch_recipes()
    for recipe in recipes:
      products = []
      
      for ingredient in np.unique(np.array(recipe["ingredients"])):
        products.append(models.Product(
          name = ingredient,
          calories = random.randint(0, 500),
          protein = round(random.uniform(2.0, 25.0), 2),
          carbohydrates	= round(random.uniform(1.0, 34.0), 2),
          fat	= round(random.uniform(0.0, 20.0), 2)
        ))
  
      recipe_obj = models.Recipe(
        name = recipe["name"],
        description = recipe["description"],
        image_url = recipe["image_url"],
        url = recipe["url"],
        products = list(products)
      )

      try:
        db.session.add(recipe_obj)
      except:
        print("Error during adding")
      
    db.session.commit()
    
  return app