from flask import Flask
from flask import request, jsonify
import graph
import optimize

app = Flask(__name__)

@app.route("/getSubscriptions")
def getSubscriptions():
    user = "rochelleli165" # request.args.get('user')
    resp = {}
    stores = graph.getSubscriptions({'id': user})
    for k in stores:
        print(k)
        resp[k] = graph.getAd({'id': k})
    return resp

@app.route("/getPantryItems")
def getPantryItems():
    user = "rochelleli165"
    resp = {}
    resp = graph.getPantryItems({'id': user})
    return resp

@app.route("/getRecipes", methods=['POST'])
def getRecipes():
    data = request.json
    ingredients = {}
    ingredients = data.get("ingredients", {})

    recipes = optimize.findRecipes(ingredients)

    return jsonify(recipes)

@app.route("/addToPantry", methods=["POST"])
def addToPantry():
    data = request.json
    print(data)
    ingredients = data.get("ingredients", {})
    user = data.get("id", "")
    graph.addToPantry({'pantry': ingredients, 'id': user})

    return jsonify({})

