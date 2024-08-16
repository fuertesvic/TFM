import sys
import networkx as nx
import numpy as np 

# Data recieved about RL and year
rl = sys.argv[1]
year = sys.argv[2]

# Root path of dataset
path = "TFM2/S2_Workspace/dataset/networks_peryear/"

# Open the specific data file
with open(f"{path}{rl}/{year}", "r") as file:
    edge_list = []
    # Read the file line by line
    for line in file:
        # Split each line into three parts using space as delimiter
        parts = line.split()
        # Convert each part into a number and create a tuple of three numbers
        edge_list.append((int(parts[0]), int(parts[1]), int(parts[2])))


def calculate_degree_centrality(edge_list):
    """Calculates the degree centrality, both local (of each node) and global (of all the network)"""
    # Retrieve the first two columns, i.e. the list of nodes
    
    network_nodes = []
    for elem in edge_list:
        network_nodes.append(elem[0])
        network_nodes.append(elem[1])

    # Calculate the frequency of each node i.e it's degree centrality.
    node_degrees = dict()
    for i in network_nodes:
        node_degrees[i] = node_degrees.get(i, 0) + 1

    # Calculate average node centrality i.e. average of degree of all network nodes.
    total = sum(list(node_degrees.values()))
    # Division by 0 protection
    avg_degree = 0
    if len(node_degrees) > 0:
        avg_degree = total/len(node_degrees)

    # Return local & global degree centrality
    return node_degrees,avg_degree

def calculate_static_metrics(edge_list):
    """Calculates the local and global clustering coefficient of the network using the networkX (nx) library"""
    # Define the graph
    G = nx.Graph()

    # Get the edges of the graph, i.e. the first two columns (timestamp isn't needed here.)
    data = [(a, b) for a, b, c in edge_list]

    # Set the graph
    G.add_edges_from(data)
    
    # Local clustering coefficient calculated by NX
    node_clustering_coef = nx.clustering(G)
    #node_closeness_centrality = nx.closeness_centrality(G)
     
    #Average clustering, with division by 0 protection
    average = 0
    if len(data)>0:
        average = nx.average_clustering(G)
    
    # Return local & global clustering coefficient.
    return node_clustering_coef,average #,node_closeness_centrality

# Calculate the metrics
node_degrees,avg_degree = calculate_degree_centrality(edge_list)    
node_clustering_coef,avg_cl = calculate_static_metrics(edge_list)

# Print on the redirected output file the static metrics: Degree centrality, Clustering Coefficient, and Closeness centrality.
# Iterate over the list of nodes, and also call the dictionary for the cl.coeff. 
for key, value in node_degrees.items(): 
    print(f"{key} {value} {node_clustering_coef[key]:0.6f}")

