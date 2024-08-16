import sys
import networkx as nx
import teneto
import pytglib as tgl
from teneto import TemporalNetwork
from teneto.networkmeasures import *
import numpy as np
import math

def crop_array_first_nonzero(array):
    """Recieves an array, finds (starting from left) the first non-zero value, and returns the array cropped, starting from that value"""
    index = (array!=0).argmax()
    return array[index:]

def calculate_node_growth(array):
    """Recieves an array with the citations of a node over the years, and returns its growth rate"""    
    if (len(array)<=1): score = array[0]
    else:
        score = []
        for i in range(len(array)-1):
            score.append(abs(array[i+1]-array[i]))
        score = sum(score)/len(array)
    return score

def calculate_dynamic_influence(array):
    ko = sum(array)
    weighted_citations = []
    for i,value in enumerate(array):
        time = len(array) - i - 1
        weighted_citations.append(value*math.exp(-time/ko))
    return sum(weighted_citations)

# Data recieved about RL and year
rl = sys.argv[1]
year = sys.argv[2]

# Root path of dataset
path = "TFM2/S2_Workspace/dataset/networks_peryear_rd/"

# Open the specific data file
with open(f"{path}{rl}/{year}", "r") as file:
    ls_of_tuples = []
    # Read the file line by line
    for line in file:
        # Split each line into three parts using space as delimiter
        parts = line.split()
        # Convert each part into a number and create a tuple of three numbers
        ls_of_tuples.append((int(parts[0]), int(parts[1]), int(parts[2])))


# Teneto Network setup
C = {'contacts': ls_of_tuples,
    'nettype': 'bu'   ,               # Binary, Undirected
    'netshape': (1,1,1),     # (This is not used but it's needed to define network)
    't0': 0,                 # Initial time
    'nodelabels': ['A', 'B'],   # Node Labels
    'timeunit': 'years'}

# Initialise Network
mynet = TemporalNetwork(from_edgelist = ls_of_tuples, nettype = 'bu')

# Calculate Temporal Degree Centrality, i.e. the citations that each node has gained each year (Returns a NxT ndarray)
# where N is the amount of nodes and T the amount of timestamps (years) 
temp_deg_cent = temporal_degree_centrality(mynet,calc='pertime')

# Eliminate node 0 since we are not using it.
temp_deg_cent = temp_deg_cent[1:]

# Import Temporal Graph file as an ordered edge list
tgs = tgl.load_ordered_edge_list(f"{path}/{rl}/{year}")


# Convert edge list to Incidence list to compute centrality measures
tg = tgl.to_incident_lists(tgs)

# Compute temporal graph metrics
# Clustering Coefficient
c_c = tgl.temporal_clustering_coefficient(tg, tg.getTimeInterval())

# Compute temporal centrality measures
# Closeness Centrality
c_cen = tgl.temporal_closeness(tgs, tgl.Distance_Type.Fastest)

# Temporal Katz
katz_cen = tgl.temporal_katz_centrality(tgs,1)

# Go over all nodes, for each one crop the array if needed, calculate and print the node growth, dynamic influence alongside the temporal degree centrality.
for i,el in enumerate(temp_deg_cent,start=1):
    values = crop_array_first_nonzero(el)
    growth = calculate_node_growth(values)
    influence = calculate_dynamic_influence(values)
    print(f"{i} {growth} {influence} {c_c[i-1]:0.6f} {c_cen[i-1]:0.6f} {katz_cen[i-1]:0.6f} {values[-1]}")
   

