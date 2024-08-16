# Enter the citations folder
path="TFM2/S2_Workspace/dataset/citations/"

# Iterate over every citation file 
for RL in `ls $path`
do 
	# Sort the file by the third column (year of cite) and store that data in a temporal file
	cat $path$RL | sort -g -k3 > tmp
	
	# Look for the year of start of that RL
	minyear="$(awk '/'"${RL}"'/ {print $2}' TFM/S2_Workspace/dataset/RL_list_years)"	
	
	
	# Move data from tmp file to the original file, overwriting unordered data with new ordered data.
	# Also and filtering the data that is before the year of start (minyear)
	awk -v threshold="$minyear" '$3>threshold' tmp > "$path$RL"

	# Remove the temporal file used.
	rm tmp

	# Call a python script that assigns a nodeID for every paperId stored in the citations file
	# This script replaces the paperIds with nodeIDs, we save that data to tmp file again
	python3 -u TFM/S2_Workspace/scripts/assign_node_ids.py $RL > tmp

	# We overwrite the paperId citations with the nodeID citations
	cat tmp > "$path$RL"	
	
	# Remove temporal file used, again.
	rm tmp
done
