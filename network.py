import networkx as nx
import matplotlib.pyplot as plt
import pylab

def graphNetwork(ingredient_names, recipes, arr, sol):
    n = len(ingredient_names)
    m = len(recipes)
    G = nx.Graph()

    G.add_nodes_from(ingredient_names, bipartite=0)
    G.add_nodes_from(recipes, bipartite=1)

    valid_edges = []
    invalid_edges = []
    optimize_edges = []
    for i in range(n):
        for j in range(m):
            if arr[i][j] != 0 and sol[i][j]:
                recipe_id = recipes[j]
                ingredient_name = ingredient_names[i]
                optimize_edges.append((ingredient_name, recipe_id))
            elif arr[i][j] != 0:
                recipe_id = recipes[j]
                ingredient_name = ingredient_names[i]
                valid_edges.append((ingredient_name, recipe_id))
            else:
                recipe_id = recipes[j]
                ingredient_name = ingredient_names[i]
                invalid_edges.append((ingredient_name, recipe_id))
    G.add_edges_from(valid_edges)
    G.add_edges_from(invalid_edges)
    G.add_edges_from(optimize_edges)

    top = nx.bipartite.sets(G)[0]
    pos = nx.bipartite_layout(G, top)

    nx.draw_networkx_nodes(G, pos=pos, node_size=4)

    alphas = iter([0.5, 0, 1])
    colors = iter(['b', 'b', 'g'])
    for i in [valid_edges, invalid_edges, optimize_edges]:
        nx.draw_networkx_edges(G,pos,edgelist = i, alpha=next(alphas), edge_color=next(colors))

    pylab.show()
