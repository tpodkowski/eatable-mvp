def get_item_calories(id, calories):
  return [recipe for recipe in calories if recipe['id'] == id][0]['calories']