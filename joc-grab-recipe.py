import requests
from bs4 import BeautifulSoup
import re
from graph import getTranslation, setRecipe

def getRecipe(url):

    name = {}
    amount = {}
    unit = {}
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
    # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the section containing the ingredients
        ingredients_section = soup.find("div", class_="wprm-recipe-ingredients-container")

        if ingredients_section:
            # Find all the list items containing the ingredients
            ingredients_list_items = ingredients_section.find_all("li")
            
            ingredients = {}
            # Extract and print the ingredients
            for item in ingredients_list_items:
                # Find the span elements for amount, unit, and name
                amount_span = item.find("span", class_="wprm-recipe-ingredient-amount")
                unit_span = item.find("span", class_="wprm-recipe-ingredient-unit")
                name_span = item.find("span", class_="wprm-recipe-ingredient-name")
                
                
                # Extract the text from the span elements
                amount = amount_span.text.strip() if amount_span else ""
                unit = unit_span.text.strip() if unit_span else ""
                name = name_span.text.strip() if name_span else ""

                if name_span.find("a") and amount == "":
                    return
                
                name = re.sub(r'\s*\(.*?\)', '', name)
                name = name.replace("/", " or ")
                
                ingredient = getTranslation(name)
                if ingredient:
                    
                    id = ingredient.replace(" ", "-")
                    
                    ingredients[id] = {
                        'amount': amount,
                        'ingredient': ingredient,
                        'name': name,
                        'unit': unit
                    }
                else:
                    f = open('ingredients.txt', 'a')
                    f.write(name)
                    f.write('\n')

                # Print the ingredient information
                # print(f"{amount} {unit} {name}")
            return ingredients
        else:
            print("Ingredients section not found on the webpage.")
            return
    else:
        print("Failed to retrieve webpage. Status code:", response.status_code)
    
for i in range(1,20):
    # URL of the webpage to scrape
    url = f"https://www.justonecookbook.com/recipes/page/{i}/"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the section containing the ingredients
        recipes = soup.find_all("article", class_="post-filter post-sm post-abbr")
        
        # Extract and print the ingredients
            
        for recipe in recipes:
            recipe_title_div = recipe.find("h3")
            recipe_title = recipe_title_div.find("a").text

            # Find the span elements for amount, unit, and name
            recipe_link = recipe.find("a", class_="post-abbr-img")
        
            
            if recipe_link and 'href' in recipe_link.attrs:
                url = recipe_link['href']
                ingredients = getRecipe(url)

                if ingredients:
                    setRecipe(recipe_title, url, ingredients)

    else:
        print("Failed to retrieve webpage. Status code:", response.status_code)

