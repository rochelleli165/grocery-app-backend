from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import urllib.request
import PIL.Image
import google.generativeai as genai
import json

from graph import postAd
from datetime import datetime

# Path to your WebDriver executable (e.g., chromedriver or geckodriver)
driver_path = "/chromedriver"

# URL of the webpage with the button
url = "https://www.aldi.us/weekly-specials/our-weekly-ads/"

# Set up the Selenium WebDriver (for Chrome in this example)
driver = webdriver.Chrome()

def gemini(im):

    genai.configure(api_key='')

    model = genai.GenerativeModel('gemini-1.5-flash')

    img = PIL.Image.open(im)
    response = model.generate_content([
        """Give me the sales and deals associated with it in the list of items and their respective prices in the form of json. 
        For the name of each item add another field in json called ingredient that omits useless adjectives before the ingredient such as where they came from 
        (California Green Grapes for example, should just say grapes, and Grass-Fed Skirt Steak should just read steak). ingredient is meant to represent 
        what the grocery item would be listed at on an online recipe (For example, ALDI Savers Navel Oranges should just be oranges and Simply Nature Organic Baby Spinach
        should just be spinach. Boneless Skinless Chicken thighs should just be chicken thighs)
        """, img], stream=True)
    response.resolve()

    cleaned_text = response.text.strip('```json\n').strip('```').strip()
    cleaned_text = cleaned_text.replace('\n', '')

    try:
        parsed_data = json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {str(e)}")
        parsed_data = {}
        return

    return parsed_data


try:
    # Open the website
    driver.get(url)

    # Wait for the iframe to be present and switch to it (adjust selector as needed)
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "shopLocalPlatformFrame"))  # Change 'iframe-id' to the actual ID of the iframe or use another selector
    )
    driver.switch_to.frame(iframe)

    # Wait for the input field to be present and enter text (adjust selector as needed)
    input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "locationInput"))  # Change 'input-id' to the actual ID or use another selector
    )
    input_field.clear()  # Optional: clear the input field if needed
    input_field.send_keys("53715")  # Replace with the text you need to enter

    # Wait for the button to be clickable and then click it (adjust selector to match the button's identifier)
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button"))  # Use ID, CLASS_NAME, XPATH, etc., as needed
    )
    button.click()

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Select Aldi at 6261 McKee Road Fitchburg, WI']"))
    )
    button.click()


    print('new page')
    
    img = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "bbpimage-1"))
    )

    src_value = img.get_attribute("src")

    # Print the extracted link
    print(f"Extracted src link: {src_value}")


    urllib.request.urlretrieve(src_value, 'aldi.jpg')

    items = gemini('aldi.jpg')

    if items:
        date = datetime.today().strftime('%Y-%m-%d')
        req = {
            'id': "-O6vVI9ms7ArDrWEAnsr",
            'date': date,
            'items': items
        }
        postAd(req)


except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()

