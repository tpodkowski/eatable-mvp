def get_item_calories(id, calories):
  return [recipe for recipe in calories if recipe['recipe_id'] == id][0]['calories']