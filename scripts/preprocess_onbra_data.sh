# Preprocesses all the data that is outputted by the ONBRA script:
# Removes all the text at the beggining of the file: Processing time, description of network... etc
# Then it removes the word "Node" to show just nodeId: value (of temporal betweenness centrality)

path="TFM2/S2_Workspace/tn_metrics/bc_dyn"
# Loop over RL
for RL in `ls $path`
do
	# Loop over years
	for year in `ls $path/$RL`
	do	
		# Get the essential data from the file and move it to tmp (the +1 is cause we don't use node 0)
		cat $path/$RL/$year | grep Node | cut -c6- | sed 's/://g' > tmp
		
		# Replace the file with the processed data and remove tmp
		awk '{print $1+1,$2}' tmp > $path/$RL/$year
		rm tmp
	done
done

