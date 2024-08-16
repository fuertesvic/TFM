import sys

# Path of the data file to be read
src_path = "TFM2/S2_Workspace/dataset/citations/"

# Path for the output dictionary of paperid:nodeId
dict_path = "TFM2/S2_Workspace/dataset/dicts/"

# Specific research line is given as input to this script 
RL = sys.argv[1]

# Method to read and parse the citations file, composed of strings in the format (paper1 paper2 year) where paper1 is cited by 2
def readcitationsfile(path):
    """Reads a string file composed of 3 columns of data and parses it and return a list of 3-element tuples"""
    data = []
    with open(f"{path}",'r') as file:
        for line in file:
            # Split the three columns and assign each one
            cols = line.strip().split()
            citedid  = cols[0]
            citingid = cols[1]
            year     = cols[2]
            data.append((citedid,citingid,year))
    return data


def assign_nodeID(paperId):
    """Assigns a nodeID for every paperId and returns it. If the paperId already has a nodeID associated with it, return it directly."""
    # Acquire the global variable
    global index

    # If given paperId is not on the dict, create a new entry and return it
    if paperId not in nodeids:
        nodeids[paperId] = index
        index += 1 
        return index
    # Case where the paperId already has a nodeId
    else:
        return nodeids[paperId]

# Read the citations data 
data = readcitationsfile(f"{src_path}{RL}")

# Create a dictionary mapping every paperid (40 character string from S2) to a nodeid (int)
# First, gather the paperIds
network_nodes = []
for elem in data:
    network_nodes.append(elem[0])
    network_nodes.append(elem[1])

# Create the dictionary for mapping paperId to nodeId and the index to number the nodes    
nodeids = {}
index = 0

# Iterate everypaperId and assign a node identifyer
for elem in network_nodes:
    nodeids[elem] = assign_nodeID(elem)

# Write the dictionary onto a file under dataset/dicts
with open(f"{dict_path}{RL}",'w') as file:
    for line in nodeids.items():
        file.write(f"{line[0]} {line[1]}\n")

# Print citations data in the format nodeid nodeid year. (The output of this script will be redirected to a txt file by the .sh script that called this .py)
for line in data:
    print(f"{nodeids[line[0]]} {nodeids[line[1]]} {line[2]}")


