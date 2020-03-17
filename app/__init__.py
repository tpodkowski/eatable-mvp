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
    from app.models.models import Product, Recipe
    from app.common.scrapper import fetch_recipes
    
    from app.homepage import homepage_bp
    from app.products import products_bp
    from app.recipes import recipes_bp
    from app.menu_composer import menu_composer_bp
    from app.calculators import calculators_bp
    from app.my_fridge import my_fridge_bp

    app.register_blueprint(homepage_bp, url_prefix='/')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(recipes_bp, url_prefix='/recipes')
    app.register_blueprint(menu_composer_bp, url_prefix='/menu-composer')
    app.register_blueprint(calculators_bp, url_prefix='/calculators')
    app.register_blueprint(my_fridge_bp, url_prefix='/my-fridge')

    db.drop_all()
    db.create_all()

    recipes = fetch_recipes()
    for recipe in recipes:
      products = []

      for ingredient in np.unique(np.array(recipe["ingredients"])):
        products.append(Product(
          name=ingredient,
          calories=random.randint(0, 500),
          protein=round(random.uniform(2.0, 25.0), 2),
          carbohydrates=round(random.uniform(1.0, 34.0), 2),
          fat=round(random.uniform(0.0, 20.0), 2)
        ))

      recipe_obj = Recipe(
        name=recipe["name"],
        description=recipe["description"],
        image_url=recipe["image_url"],
        url=recipe["url"],
        products=list(products)
      )

      try:
        db.session.add(recipe_obj)
      except:
        print("Error during adding")

    db.session.commit()

  return app
