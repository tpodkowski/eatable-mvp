from flask import Blueprint, render_template, request, redirect
from app.models.models import Recipe, db
from app.common.helpers import get_item_calories

menu_composer_bp = Blueprint('menu_composer_bp', __name__,
                             template_folder='templates',
                             static_folder='static', static_url_path='assets')
  

@menu_composer_bp.route('/', methods=['GET', 'POST'])
def menu_composer():
  recipes = Recipe.query.join(Recipe.products)
  calculations = []
  result = {}
  previous_values = []
  
  if request.method == 'POST':
    form_data = list(request.form.to_dict(flat=True).items())
    user_meal_plan = list(map(lambda item: {item[0]: item[1]}, form_data))
    query = db.session.execute('''
      SELECT
        recipe_id,
        SUM(calories) as calories
      FROM
        (SELECT
          recipe.recipe_id,
          product.calories
        FROM recipe AS recipe
        JOIN recipes_products AS recipes_products ON recipe.recipe_id=recipes_products.recipe_id
        JOIN product AS product ON product.product_id=recipes_products.product_id
        GROUP BY
          recipe.recipe_id,
          product.calories
        ORDER BY recipe.recipe_id) AS Calories
      GROUP BY recipe_id
    ''')
    recipes_calories = [dict(row) for row in query]

    for item in form_data:
      day = item[0].split('-')[0]
      recipe_id = int(item[1])

      if recipe_id != -1:
        if day in result:
          result[str(day)] = result[str(day)] + get_item_calories(recipe_id, recipes_calories)
        else:
          result[str(day)] = get_item_calories(recipe_id, recipes_calories)
    
    previous_values = request.form.to_dict()
    calculations = list(result.values())

  return render_template('menu-composer/menu-composer.html', form=previous_values, recipes=recipes, calculations=calculations)
