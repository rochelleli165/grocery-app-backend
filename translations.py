import google.generativeai as genai
import json

from graph import updateTranslations


def gemini(ingredients):
    
    genai.configure(api_key='')

    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content([
        """Give me in json format the in each ingredient listed a more short and precise ingredient name. For example,
        return 
        { 'green bell pepper': 'bell pepper',  
        'green onion or scallion': 'green onion',  
        'extra virgin olive oil': 'olive oil',
        'ground pork': 'ground pork'
        }
        Descriptive words like boneless, homemade, or tap can be ignored. 
        """, ingredients], stream=True)
    response.resolve()

    
    cleaned_text = response.text.strip('```json\n').strip('```').strip()
    cleaned_text = cleaned_text.replace('\n', '')
    cleaned_text = cleaned_text.strip("```")

    try:
        parsed_data = json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {str(e)}")
        parsed_data = {}

    print({"result": parsed_data })
    return parsed_data

def update_translations():
    f = open('ingredients.txt', 'r')
    i = f.readlines()
    f.close()
    ingredientss = 20 * [""]

    for index, j in enumerate(i):
        ingredientss[(index % 19)] += (j + " ")
    for ingredients in ingredientss:
        data = gemini(ingredients)
        print(data)
        updateTranslations(data)


update_translations()