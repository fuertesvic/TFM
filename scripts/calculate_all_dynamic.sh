src_path="TFM2/S2_Workspace/dataset/networks_peryear_rd/"
output_path="TFM2/S2_Workspace/tn_metrics/dynamic/"

# For each Research Line, complete and reduced
for RL in `ls $src_path`
do
	# Make a dir only if it doesnt exist already (-p option)
	mkdir -p $output_path$RL
	for year in `ls $src_path/$RL`
	do
		# Calcualte the static network metrics for that year and save it onto a file named like the year.
		# The python Script recieves as parameters the RL and the year.
		python3 -u TFM2/S2_Workspace/scripts/calculate_dynamic_metrics.py $RL $year > $output_path$RL/$year
	done
done

~
