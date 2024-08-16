import requests
import json
import sys

input_path  = "TFM2/S2_Workspace/dataset/paper_list/"
output_path = "TFM2/S2_Workspace/dataset/citations/"
def read_json_file(filename):
    """Reads a JSON file"""
    with open(filename, 'r') as file:
        data = json.load(file)
    return data 

def filter_relevant_papers(data,threshold=1):
    """Filters papers, remove papers that have citationCount < threshold"""
    filtered_data = {}
    for item in data:
        if data[item]['citationCount'] > threshold:
            filtered_data[item] = data[item]
    return filtered_data   

def group_papers_1k_citations(data):
    """Gets a dictionary of papers, groups them into lists of paperIDs that have a sum of
    citationCounts lower than 1000, which is the max nº of citations that API can return in
    a single call. Returns a list of lists."""
    # Setup a counter for counting 1000 citations.
    cnt = 0 

    # Initialize lists
    paperchunks_list = []
    paperchunk = []

    # Loop over all papers in the dictionary.
    for paperid in data:
        citcount = data[paperid]['citationCount']

        # If paper has more than 1k citations, it has to appear multiple times on the list.
        if citcount > 1000:
        
            paperchunks_list.append([paperid])
                
        # Less than 1k citations per paper case
        else:
            # Append paper to chunk if the citations of the chunk + the new paper are less than 1000.
            if (cnt + citcount < 1000) & (len(paperchunk) < 500):  
                paperchunk.append(paperid)
                cnt += citcount
            # If it doesn't fit on the chunk, store that chunk and create a new one.
            else:
                paperchunks_list.append(paperchunk)
                cnt = citcount
                paperchunk = []
                paperchunk.append(paperid)

    # Case for finish, when there are no new papers that trigger the last else condition.
    paperchunks_list.append(paperchunk)    

    return paperchunks_list  

def assign_nodeID(paperId):
    """Assigns a nodeID to a input paperID, unless there was already a node with that paperID"""
    global index
    if paperId not in nodeIDs:
        nodeIDs[paperId] = index 
        index += 1
        return index
    else:
        return nodeIDs[paperId]

def build_dyn_network():
    """Reads the data of a JSON file containing a list of papers; checks  citations,
    numbering each citing paper a node identifyer which is 1 more than the last one. Then it writes to a file the citation,
    in the form (cited node) (citing node) (year of cite) Example: If paper A has 3 cites and B has 2, this function will print to file
    the following:
    1 2 20XX
    1 3 20XX
    1 4 20XX
    5 6 20XX
    5 7 20XX"""

    # Read the JSON with the list of papers
    data = read_json_file(f'{input_path}{query}.json')

    # Groups the papers in chunks of papers that have ~~1k citations (maximum output of API)
    paperIDs_list_of_chunks = group_papers_1k_citations(data)
    
    # Batch Search allows the user to ask the API for data of 500 papers at once. (Returns maximum 1k citations)
    url = "https://api.semanticscholar.org/graph/v1/paper/batch"

    with open(f'{output_path}{query}','w') as f:   

        # tIerate over every chunk of paperIDs
        for paperchunk in paperIDs_list_of_chunks:

            #print(f"\nProcessing {len(paperchunk)} Paper(s) of {query} dynamic network")
            r = requests.post(url,headers=headers,params=query_params,json={"ids":paperchunk})

             # Check that API's response is correct
            if r.status_code == 200:
                r = r.json() 
                
                # Response comes as a list of dicts, each paperId has its own dictionary containing paperid, title, and citations.
                for paper in r:
                    # Retrieve the paperId of the cited paper and assign it a new node.
                    if paper is not None:
                        citedid = paper['paperId']
              
                        #citednode = assign_nodeID(citedid)

                        # Iterate over every citation of the specific paper and assign the citing paperID a nodeID.
                        for cite in paper['citations']:

                            # Check that the 'year' information is availabe.
                            if (cite['year']) is not None:
                                citingid = cite['paperId']
                                #citingnode = assign_nodeID(cite['paperId'])
                                f.write(f"{citedid} {citingid} {cite['year']}\n") 
            #else:
                #print(f"API error: {r}")

def build_rd_dyn_network():
    """Reads the data of a JSON file containing a list of papers; looks for the citations of each of them, and 
    every citing paper is checked if it's on the JSON dataset. If the citing paper is on the database, the citation is 
    stored in the same way as the previous function, i.e
    (citednode) (citingnode) (yearofcite).
    Here, the node identifyers are the ones in the JSON dataset.    
    """

    # Read the JSON with the list of papers
    data = read_json_file(f'{input_path}{query}.json')

    # Groups the papers in chunks of papers that have ~~1k citations (maximum output of API)
    paperIDs_list_of_chunks = group_papers_1k_citations(data)
    
    # Batch Search allows the user to ask the API for data of 500 papers at once. (Returns maximum 1k citations)
    url = "https://api.semanticscholar.org/graph/v1/paper/batch"

    # Open the file.    
    with open(f'{output_path}{query}_rd','w') as f:   

        # Iterate over every chunk of paperIDs
        for paperchunk in paperIDs_list_of_chunks:

            # Debugging
            # print(f"\nProcessing {len(paperchunk)} Paper(s)  {query} (restricted) dynamic network")
            r = requests.post(url,headers=headers,params=query_params,json={"ids":paperchunk})

            # Check that API's response is correct
            if r.status_code == 200:
                r = r.json() 

                # Response comes as a list of dicts, each paperId has its own dictionary containing paperid, title, and citations.
                for paper in r:

                    # Retrieve the paperId and the internal nodeID
                    citedid = paper['paperId'] 
                    citednode = data[citedid]['nodeID']

                    # Iterate over every citation, and check if it is on the internal dataset and information abt year is available.
                    for cite in paper['citations']:
                        if (cite['paperId'] in data) & (cite['year'] is not None):
                            
                            # Retrieve the nodeID of the citing paper.
                            #citingnode = data[cite['paperId']]['nodeID']
                            citingid = cite['paperId']
                            # Write on file the edge between two nodes.
                            f.write(f"{citedid} {citingid} {cite['year']}\n") 

            # Incorrect API response case.
            #else:
                #print(f"API error: {r}")

# Set parameters to query API, including the API key, query for citations
api_key = 'zxHPpAOUse8P7Zz5mHJSo4J3i0d17Csd3bwTGfMA'
headers = {'x-api-key': api_key}
query_params = {'fields': 'paperId,year,citations.year'}

# Set dictionary for assigning each paper a nodeID for the dynamic network (Not restricted).
nodeIDs = {}
index = 0       

if __name__ =='__main__':
    query = sys.argv[1]
    build_dyn_network()
    build_rd_dyn_network()
