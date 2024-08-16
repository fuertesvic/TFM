REPOSITORY FOR THE PAPER "Metric Comparison for Temporal Graphs in Research Trends Networks"
by Víctor Fuertes (Tutor: Carlos Borrego Iglesias)

This repository contains:

i)  Dataset: (18*2) Academic Temporal Networks as edge lists -- S2_Workspace/dataset/networks_peryear/ 
ii) Scripts used & mentioned in the paper M&M section: -- S2_Workspace/scripts/
	ii.a) Obtain the dataset
	ii.b) Filter, Sort and NodeID assignation
	ii.c) Temporal Graph building
	ii.d) Calculation of static metrics
	ii.e) Calculation of dynamic metrics
	ii.f) Data processing for constructing a data file with all metrics combined

iii) Temporal Network Metrics: for all RL's (complete&reduced) for every year, for every node, static metrics and dynamic metrics -- S2_Workspace/tn_metrics/static
	     S2_Workspace/tn_metrics/dynamic

iv) Script to implement XGBOOST to extract feature importance on the gradient descent booster

v)  Final results in a txt file

vi) Python Script to visualize the feature importance in a bar plot. 


DATA STRUCTURE

Root Directory: S2_Workspace (from Semantic scholar, known as S2):

S2_Workspace Folders: 

	scripts:

		- create_paperlist_dataset.py -- Used to acquire the list of papers.
		Called directly from terminal with the query parameters to call S2 API. Stores JSON with paper data (paperId, title, year, citationCount) under the directory /dataset/paper_list.
		Input format: 
			- Query: (quoted, usually: "bitcoin", or "opportunistic network")
			- Filename: name of the file for storing the data. Usually an abbreviation i.e. btc.
			- Year 1, year 2. Usually 2000 2024.


		- get_dyn_net.py	     -- Reads data from the paper list created previously. 
		For each paper, asks the API for the data of it's citations. It assigns each paper node number, and stores every citation with the year. It stores on a text file under dataset/citations in 
		the format: 1 2 2000, as in node 1 (cited node) node 2 (citing node) year (of citation)
		This python file is called from the next shell script, it's not supposed to be called manually.

		- get_networks.sh   -- For each research line (enters the paper_list folder to check), calls the python script "get_dyn_net.py" to build the citations data.



		- sort_by_year.sh  -- Enters the dataset/citation folder and sorts by year (by the third column) every file. This script must be executed after get_networks.sh



		- build_networks_per_year.sh  -- To build the temporal networks, takes every citation file for each research line and builds 24 files, starting from 2000 untill 2024, 
		separating the data. For every research line, it creates a folder on dataset/peryear/, and inside the folder created, creates 24 files. The first, 2000, contains the data of the network 
		untill 2000. The second one, the data untill 2001, third, data untill 2002... etc.

		
		- calculate_static_metrics.py   :  Script to calculate static metrics. Reads data from dataset/networks_peryear, writes data into tn_metrics/static
		- calculate_dynamic_metrics.py  :  Same thing for dynamic metrics. tn_metrics/dynamic
		
	dataset:
		-RL_list_years : file containing the details about what year each RL starts

		-paper_list : contains the data acquired directly from API, i.e. the papers themselves with their title, paperId, year of publication and amount of cites. Also, an internal node ID
			      each RL has its own file.
		-citations  : edges data of the networks. For every paper, checked their citations and stored. Reduced networks and complete networks
		
		-networks_peryear:   the edge lists but separated per year. For example, BTC RL starts on 2008, so there will be a "2008" file with the edges up untill 2008, another called "2009"
					with the network edges untill 2009, and so on.

	tn_metrics:
		- static_metrics: local & global static degree centrality &  static cluster coefficient. THere is a file for each year, and each file contains a list of nodes, 
					with the local metrics, and in the end of the file there are global metrics indicated.

		- dynamic_metrics: local & global dynamic degree centrality & dynamic betweenness centraluty with ONBRA
	  

					 
