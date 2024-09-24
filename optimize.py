from gurobipy import Model, GRB
import gurobipy as gp
from graph import getAllRecipes
from network import graphNetwork


def findRecipes(ingredients):

    print(ingredients)
    pantry_items = ingredients
    # Create a new Gurobi model
    model = Model("OptimizationExample")

    raw_recipes = getAllRecipes()

    all_ingredients_map = {}
    index = 0
    for recipe in raw_recipes:
        ingredients = raw_recipes[recipe]['ingredients']
        for i in ingredients:

            if i not in all_ingredients_map:
                all_ingredients_map[i] = index
                index += 1
    
    all_ingredients = list(all_ingredients_map.keys())

    recipes = list(raw_recipes.keys())

    n = len(all_ingredients)
    m = len(recipes) 
    o = len(pantry_items)

    arr = [[0 for x in range(m)] for y in range(n)] 
    supply = [0] * n
    demand = [0] * m
    recipe_titles = [0] * m
    for i in range(n):
        ingredient_name = all_ingredients[i]
        for j in range(m):
            recipe_id = recipes[j]
            if ingredient_name in raw_recipes[recipe_id]['ingredients']:
                arr[i][j] = 1
            if ingredient_name in pantry_items:
                supply[i] = 2
    for i in range(m):
        recipe_id = recipes[i]
        demand[i] = len(list(raw_recipes[recipe_id]['ingredients']))
        recipe_titles[i] = raw_recipes[recipe_id]['recipe-title']

    # Define decision variables: x1 and x2 are non-negative
    x = model.addVars(n, m, vtype=GRB.CONTINUOUS, name="x", lb=0)
    y = model.addVars(m, vtype=GRB.BINARY, name="y", lb=0)
    
    # Add constraints
    model.addConstrs(
        (x[i,j] <= arr[i][j] for i in range(n) for j in range(m)),
        name="supply_constraint"
    )

    model.addConstrs(
        (gp.quicksum(x[i,j] for j in range(m)) <= supply[i] for i in range(n)),
        name="supply_constraint"
    )

    model.addConstrs(
        (gp.quicksum(x[i,j] for i in range(n)) - demand[j] <= 10*demand[j]*y[j] - (1-y[j]) for j in range(m)),
        name="demand_constraint"
    )

    model.addConstrs(
        (gp.quicksum(x[i,j] for i in range(n)) - demand[j] >= -10*demand[j]*(1-y[j]) for j in range(m)),
        name="demand_constraint"
    )

    # Set the objective function: maximize 3x1 + 4x2
    model.setObjective(gp.quicksum(y[j] for j in range(m)), GRB.MAXIMIZE)

    # Optimize the model
    model.optimize()

    # Display the results
    sol_recipes = []
    if model.status == GRB.OPTIMAL:
        print("Optimal Objective Value:", model.objVal)
    else:
        print("No optimal solution found.")

    sol = [[0 for x in range(m)] for y in range(n)] 
    for i in range(n):
        for j in range(m):
            x = model.getVarByName(f"x[{i},{j}]")
            sol[i][j] = x.X
    for j in range(m):
        y = model.getVarByName(f"y[{j}]")
        if y.X == 1.0:
            sol_recipes.append(recipe_titles[j])
    print(sol_recipes)
    #graphNetwork(pantry_items, recipes, arr, sol)

    return sol_recipes


findRecipes(["soy-sauce", "water", "cabbage", "black-pepper", "carrot", "chicken-thigh", 
             "green-onion", "katsuobushi", "mentsuyu", "oil", "onion", "udon", "toppings",
             "mirin", "sugar", "dashi", "salt"
             ])
