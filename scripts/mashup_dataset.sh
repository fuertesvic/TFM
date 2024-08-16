# Joins the data from the static  metrics, dynamic metrics, and ONBRA betweenness centrality into a single table
# Each one of the three mentioned above are in different files under different folders.
input_path="TFM2/S2_Workspace/tn_metrics"
output_path="TFM2/xgboost/final_datasets_complete"

# Loop over all RLs
for RL in `ls $input_path/static`
do	
	# Create file for combined data, aka the final dataset.
	out_file=$output_path/$RL
	

	# Loop over years
	for year in `ls $input_path/static/$RL`
	do
		# Set the paths for the 3 data files to take data from
		sta_file=$input_path/static/$RL/$year
		dyn_file=$input_path/dynamic/$RL/$year
		dbc_file=$input_path/bc_dyn/$RL/$year

		# Remove the first column of the dynamic data (the nodeId column) since otherwise it would be duplicated 
		# From the dynamic betweenness centrality, only get the 2nd column; the bc value
		cut -d ' ' -f2 $dbc_file > tmp

		# From the dynamic metrics file, get columns 2,3,4,5,6,7 which are DG,DI,DClC,DCC,Katz,DDC (Target)
		cut -d ' ' -f2-7 $dyn_file > tmp1
	
		# Join the lines from static, dynamic and bcd files withouth the node column
		paste -d ' ' $sta_file tmp tmp1 > tmp2
		
		# The result so far is the temporal network of one year, so this line prints the year as a constant first column
		awk -v yr="$year" '{print yr, $0}' tmp2 | sed 's/://g' > tmp3

		# Append the temporal network of that year to the final dataset where all years are collected
		cat tmp3 >> $out_file
		
		
	done
	rm tmp
	rm tmp1
	rm tmp2
	rm tmp3
done
