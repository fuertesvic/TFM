import requests
import json
import sys

output_path = "TFM2/S2_Workspace/dataset/paper_list/"

# Set query parameters for API.
api_key = 'zxHPpAOUse8P7Zz5mHJSo4J3i0d17Csd3bwTGfMA'
headers = {'x-api-key': api_key}
fields = 'citationCount,title,year'

def get_paper_list_bulk():
    """Calls Semantic Scholar API with a bulk search and stores all papers found
    in a .JSON file. Multiple text queries and range years are allowed. Gets paperId, title,
    year and citationcount, but not the citations themselves."""         
    
    # Set url with query, name for the result file.
    url = f"http://api.semanticscholar.org/graph/v1/paper/search/bulk?query={query}&fields={fields}&year={year1}-{year2}"

    # First Call to API
    r = requests.get(url,headers=headers).json()
    retrieved = 0 
    data_list = {}
    print(f"\nTotal Papers found for Search: {query} from years {year2} - {year1}: {r['total']}")
    
    # Navigate API's response pages
    while True:
        if "data" in r:
            for i,paper in enumerate(r["data"]):
                data_list |= {paper['paperId']: paper}        # Store Data 
            retrieved += len(r["data"])
            print(f"Retrieved {retrieved} papers...")           

        if 'token' not in r:    # If no more pages, stop
            break

        newurl = f"{url}+&token={r['token']}"               # Add token to search next page of results
        r = requests.get(newurl,headers=headers).json()     # New call adding token.  
        
        # Sort by citation Count
        data_list_sorted = sorted(data_list.items(), key = lambda item: item[1]['year'],reverse=False)
        sorted_dict = {item[0]:item[1] for item in data_list_sorted}
        filtered = {k:v for k,v in sorted_dict.items() if v['citationCount'] > 0}

        for i,paper in enumerate(filtered.values()):
            paper['nodeID'] = i

        # Write data into json file.
        with open(f"{output_path}{filename}.json", "w", encoding="utf-8") as file:
            json.dump(filtered,file,indent=2)
    
if __name__ == '__main__':
    if len(sys.argv) == 5:
        _,query,filename,year1,year2 = sys.argv
        get_paper_list_bulk()
    else:
        print(f"Errors, parameters must be query - filename - year1 - year2, please try again")
   
    
