REPOSITORY FOR THE PAPER "Metric Comparison for Temporal Graphs in Research Trends Networks"
by Víctor Fuertes (Tutor: Carlos Borrego Iglesias)

This repository contains the scripts used for the study (in the M&M section of the paper)

DATASET ACQUISITION SCRIPTS:
I) create_paperlist_dataset.py -- Called directly from terminal with the query parameters to call S2 API. Stores JSON with paper data (paperId, title, year, citationCount) under the directory /dataset/paper_list.
	Input format: 
	- Query: (quoted, usually: "bitcoin", or "opportunistic network")
	- Filename: name of the file for storing the data. Usually an abbreviation i.e. btc.
	- Year 1, year 2. Usually 2000 2024.

II.a) get_dyn_net.py	-- Reads data from the paper list created previously. 
	For each paper, asks the API for the data of it's citations. It assigns each paper node number, and stores every citation with the year. It stores on a text file under dataset/citations in 
	the format: 1 2 2000, as in node 1 (cited node) node 2 (citing node) year (of citation)
	This python file is called from the next shell script, it's not supposed to be called manually.

II.b) get_networks.sh   -- For each research line (enters the paper_list folder to check), calls the python script "get_dyn_net.py" to build the citations data.

III)  sort_by_year.sh  -- Enters the dataset/citation folder and sorts by year (by the third column) every file. This script must be executed after get_networks.sh

IV) assign_node_ids.py 

V)   build_networks_per_year.sh  -- To build the temporal networks, takes every citation file for each research line and builds 24 files, starting from 2000 untill 2024, 
		separating the data. For every research line, it creates a folder on dataset/peryear/, and inside the folder created, creates 24 files. The first, 2000, contains the data of the network 
		untill 2000. The second one, the data untill 2001, third, data untill 2002... etc.


NETWORK METRIC SCRIPTS

VI.a)   calculate_static_metrics.py   :  Scripts to calculate static metrics. Reads data from dataset/networks_peryear, writes data into tn_metrics/static
VI.b)   calculate_all_static.sh
VI.c)   calculate_dynamic_metrics.py  :  Same thing for dynamic metrics. tn_metrics/dynamic
VI.d)   calculate_all_dynamic.sh

VII.a) Onbra_betweenness_centrality.sh
VII.b) preprocess_onbra_data.sh


DATA PROCESSING, ML ANALYSIS, AND RESULTS VISUALIZATION

VIII) mashup_dataset.sh
IX.a) calculate_FI_complete.py
IX.b) calculate_FI_reduced.py
X.a) visualize_results_complete.py
X.b) visualize_results_reduced.py
