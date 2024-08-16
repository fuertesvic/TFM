src_path="TFM2/S2_Workspace/dataset/networks_peryear/"
output_path="TFM2/S2_Workspace/tn_metrics/static/"
# For each Research Line, complete and reduced
for RL in `ls $src_path`
do
	# Debugging Info
	echo "Processing $RL"

	# Make a dir only if it doesnt exist already (-p) option
	mkdir -p $output_path$RL
	for year in `ls $src_path/$RL`
	do
		# More debugging info
		echo $year
		# Calcualte the static network metrics for that year and save it onto a file named like the year.
		# The python Script recieves as parameters the RL and the year.
		python3 -u TFM2/S2_Workspace/scripts/calculate_static_metrics.py $RL $year > $output_path$RL/$year
	done
done
