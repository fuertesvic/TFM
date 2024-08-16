SCRIPT STEPS IN ORDER

A -- Build Papers dataset

i)  create_paperlist_dataset.py with args {query} {filename} {startyear} {endyear}


B -- Generate citations temporal networks and process them

ii) get_networks.sh

iii) sort_by_year.sh

iv) build_networks_per_year.sh


C -- Calculate the static & dynamic network measures

v) calculate_all_static.sh

vi) calculate_all_dynamic.sh

vii) onbra_betweenness_centrality.sh

viii) preprocess_onbra_data.sh


D -- Join all data into a single data file

ix) mashup_dataset.sh  -- creates one file for each RL

x)  mash_all_datsets.sh -- creates a single macro file for all RL's



E -- Process the data with XGBOOST

outside this scripts directory... under TFM/xgboost

 
