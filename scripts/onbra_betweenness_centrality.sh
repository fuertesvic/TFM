# Paths for input, output, and c script to calculate temporal betweenness centrality
src_path="TFM2/S2_Workspace/dataset/networks_peryear"
out_path="TFM2/S2_Workspace/tn_metrics/bc_dyn"
onbra_path="TFM2/onbra/build.build/onbra"

# Loop over all RL's
for RL in `ls $src_path`
do
	echo "Processing $RL" # Debugging info about the progress of the computations
	
	# Make a dir only if it doesnt exist already (-p option)
	mkdir -p $out_path/$RL

	# Loop over all years
	for year in `ls $src_path/$RL` 
	do
		echo $year # Debug info 
		# Call the executable file located in the onbra path with a file (-f) as input, the file located at src_path and redirect output to out_path	
		./$onbra_path -f $src_path/$RL/$year -E 1 -S 3000 > $out_path/$RL/$year  
	done 
done

