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

IV) assign_node_ids.py -- (Called by sort_by_year.sh) replaces the 40-character strings from the paperId for a unique new local identifyer which is an integer number to every paper (nodeID)

V)   build_networks_per_year.sh  -- To build the temporal networks, takes every citation file for RL and builds n files, starting from [start year of RL] untill 2024, 
		separating the data. For every RL, creates a folder on dataset/peryear/, and n files with filename as the year. For example: first file, called '2000', contains the data of the network 
		untill 2000. The second one, named 2001, the data untill 2001, third, data untill 2002... etc.


NETWORK METRIC SCRIPTS

VI.a)   calculate_static_metrics.py   :  Scripts to calculate static metrics. Reads data from dataset/networks_peryear. It uses networkX libraries and own code for the metrics
VI.b)   calculate_all_static.sh	      :  Bash script that enters the networks_peryear dataset folder, and for every RL (both compl. and reduced) calls the prev. py script to compute the metrics and redirects its 					 output to S2_Workspace/tn_metrics/static
VI.c)   calculate_dynamic_metrics.py  :  Same thing for dynamic metrics. It uses mainly TGLIB library.
VI.d)   calculate_all_dynamic.sh      :  Same as VI.b)

VII.a) Onbra_betweenness_centrality.sh	: Bash script that iterates over dataset and calls the C program to 
VII.b) preprocess_onbra_data.sh		: Filters out the output file of the ONBRA program: it removes some unwanted text and formats it to our format which is txt file with 2 cols: first for the node and second 					  for the betweenness_centrality value. It stores the data under tn_metrics/bc_dyn 


DATA PROCESSING, ML ANALYSIS, AND RESULTS VISUALIZATION

VIII) mashup_dataset.sh			-- Builds a file where all the temporal networks are joined in a single table. Its columns are: year, node, metric1, metric2, ...metric10
IX.a) calculate_FI_complete.py		-- Calculate feature importance for complete networks, training XGBOOST model. It returns two files as tables where each row is a RL, and each column is a metric where
					the gain is shown for every metric in one file, and in the other, the weight is shown.
IX.b) calculate_FI_reduced.py		-- Same for reduced networks. It's a differnet file because there are metrics that are only computed on the reduced networks due to computation complexity.
X.a) visualize_results_complete.py	-- Creates the bar plots for visualizing feature importance. It also performs the statistical tests using scipy.stats library
X.b) visualize_results_reduced.py	-- Same for reduced networks.
