import requests
import json
import os
from bs4 import BeautifulSoup

def get_image_url(soup):
  return soup.find("div", { "class": "recipe-preview-image" }).find("img")['data-src']


def get_ingredients(soup):
  ingredients = []
  lis = soup.find("ul", { "class": "ingredient-ul" }).find_all("li", { "class": "ingredient-li" })
  for li in lis:
    ingredients.append(li.find("div", { "class": "ingredient-name" }).get_text())

  return ingredients


def get_steps(soup):
  steps = []
  steps_elements = soup.find("div", { "class": "recipe-container-steps" }).find_all("li")

  for step in steps_elements:
    steps.append({
      "title": step.find("span", { "class": "step-responsive-header" }).get_text(),
      "text": step.find("div", { "class": "step-responsive-text" }).get_text(),
    })

  return steps


def fetch_recipes():
  PAGES_TO_FETCH = 1
  recipes = []
  error_count = 0

  has_recipes = os.path.isfile('recipes.dat')

  if not has_recipes:
    for page in range(PAGES_TO_FETCH):
      url_response = requests.get(os.environ["OBIAD_URL"] + str(page))
      page_soup = BeautifulSoup(url_response.text, 'html.parser')
      recipes_elements = page_soup.find_all("a", { "class": "recipe-box__title" })
      
      for recipe in recipes_elements:
        recipe_url = recipe["href"]
        response = requests.get(recipe_url)
        recipe_soup = BeautifulSoup(response.text, 'html.parser')
        try:
          recipe_obj = {
            "url": recipe_url,
            "name": recipe.get_text(),
            "image_url": get_image_url(recipe_soup),
            "ingredients": get_ingredients(recipe_soup),
            "description": get_steps(recipe_soup)
          }
          recipes.append(recipe_obj)
        except:
          error_count += 1
          print("[ERROR] " + recipe_url)    
    
    with open('recipes.dat', 'w') as json_file:
      json.dump(recipes, json_file)
    print("\nSuccesfuly added: " + str(len(recipes)) + ", " + str(error_count) + " skipped\n")
  else:
    recipes = json.loads(open('recipes.dat', 'r').read())
  
  print(recipes)
  return recipes
