import requests
from bs4 import BeautifulSoup

def get_title(soup):
  return soup.find("h1", { "class": "title" }).get_text()


def get_image_url(soup):
  return soup.find("div", { "class": "recipe-preview-image" }).find("img")['data-src']


def get_ingredients(soup):
  ingredients = []
  lis = soup.find("ul", { "class": "ingredient-ul" }).find_all("li", { "class": "ingredient-li" })
  for li in lis:
    ingredients.append({
      "name": li.find("div", { "class": "ingredient-name" }).get_text(),
      "quantity": li.find("span", { "class": "quantity" }).get_text(),
    })
  return ingredients


def get_description(soup):
  description = ""
  lis = soup.find("div", { "class": "recipe-container-steps" }).find_all("li")
  for li in lis:
    description += li.get_text() + " "
  
  return description


def fetch_recipes():
  PAGES_TO_FETCH = 1
  recipes = []
  error_count = 0

  for page in range(PAGES_TO_FETCH):
    url_response = requests.get("https://www.przepisy.pl/przepisy/posilek/obiad?page=" + str(page))
    page_soup = BeautifulSoup(url_response.text, 'html.parser')
    recipes_elements = page_soup.find_all("div", { "class": "recipe-box-5-container" })
    
    for recipe in recipes_elements:
      recipe_url = recipe["data-recipeurl"]
      response = requests.get(recipe_url)
      recipe_soup = BeautifulSoup(response.text, 'html.parser')
      
      try:
        recipe_obj = {
          "url": recipe_url,
          "name": get_title(recipe_soup),
          "image_url": get_image_url(recipe_soup),
          "ingredients": get_ingredients(recipe_soup),
          "description": get_description(recipe_soup)
        }
        recipes.append(recipe_obj)
      except:
        error_count += 1
        print("[ERROR] " + recipe_url)

  print("\nSuccesfuly added: " + str(len(recipes)) + ", " + str(error_count) + " skipped\n")
  return recipes

# print(fetch_recipes())