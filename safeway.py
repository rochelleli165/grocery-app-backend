import requests

# Specify the URL
url = 'https://backflipp.wishabi.com/flipp/items/search?locale=en&postal_code=94539&q=walmart'

# Make the GET request
response = requests.get(url)

# Raise an error if the request was unsuccessful
response.raise_for_status()

# Parse the response content as JSON
response_json = response.json()

# Access and print the 'items' key in the JSON response
if 'items' in response_json:
    for item in response_json['items']:
        if '_L2' in item and (item['_L2'] == 'Food Items' or item['_L2'] == 'Beverages'):
            if item['current_price'] == None:
                print(item['name'], " ", item['sale_story'])
            else:
                print(item['name'], " ", item['current_price'])
else:
    print('No items found in the response.')
