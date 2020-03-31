import requests
import json
import os
from bs4 import BeautifulSoup
import pprint

def get_image_url(soup):
  return soup.select_one('.recipe-image > img')['src']


def get_ingredients(soup):
  ingredients = []
  lis = soup.find("div", { "class": "ingredients" }).find_all("li")
  for li in lis:
    ingredients.append(li.get_text())

  return ingredients


def get_steps(soup):
  steps = []
  steps_elements = soup.find("div", { "class": "steps" }).find_all("li")
  step_index = 1

  for step in steps_elements: 
    steps.append({
      "title": "Krok " + str(step_index),
      "text": step.get_text(),
    })
    step_index+=1

  return steps

def add_domain_name(slug):
  return os.environ["SCRAPPING_DOMAIN_URL"] + slug


def fetch_recipes():
  PAGES_TO_FETCH = 1
  recipes = []
  error_count = 0

  has_recipes = os.path.isfile('recipes.dat')

  if not has_recipes:
    print('Scrapping started')
    for page in range(1, PAGES_TO_FETCH + 1):
      response = requests.get(add_domain_name(os.environ["DINNER_URL"]) + str(page))
      page_soup = BeautifulSoup(response.text, 'html.parser')
      recipes_elements = page_soup.select_one('app-header-recipe-list + div').find_all("a", { "class": "recipe-box__title" })
      
      for recipe in recipes_elements:
        recipe_url = add_domain_name(recipe["href"])
        response = requests.get(recipe_url)
        recipe_soup = BeautifulSoup(response.text, 'html.parser')
        print_page_url = add_domain_name(recipe_soup.select_one('app-recipe-page-tools a')["href"])
        
        static_page = requests.get(print_page_url)
        static_page_soup = BeautifulSoup(static_page.text, 'html.parser')

        try:
          recipe_obj = {
            "url": recipe_url,
            "name": recipe.get_text(),
            "image_url": get_image_url(static_page_soup),
            "ingredients": get_ingredients(static_page_soup),
            "description": get_steps(static_page_soup)
          }
          print(recipe_obj)
          recipes.append(recipe_obj)
        except:
          error_count += 1
          print("[ERROR] " + recipe_url)    
    
    with open('recipes.dat', 'w') as json_file:
      json.dump(recipes, json_file)
    print("\nSuccesfuly added: " + str(len(recipes)) + ", " + str(error_count) + " skipped\n")
  else:
    recipes = json.loads(open('recipes.dat', 'r').read())
  
  return recipes
