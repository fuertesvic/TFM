source_path="TFM2/S2_Workspace/dataset/citations/"
destination_path="TFM2/S2_Workspace/dataset/networks_peryear/"

# Go over all files of "Citations" Folder. (all the networks)
for RL in `ls $source_path`
do
	# Create a folder, (only if it doesn't exists, -p) for that Research Line (One for whole network, other for Reduced)
	mkdir -p $destination_path$RL

	# Find starting Year of RL on the txt file that stores the starting year of each one.
	minyear="$(awk '/'"${RL}"'/ {print $2}' TFM/S2_Workspace/dataset/RL_list_years)"

	# Iterate over years from specific starting year to 2024	
	for year in `seq $minyear 2024`
	do 
		# Export variables year &minyear to use it in AWK 
		export yr=$year
		export minyear=$minyear

		# Save on a new file (called *Year*) the state of the network (citations) untill year *Year*, filtering out everything before that year
		cat $source_path/$RL | awk -v year=$yr '{if (year>$3) print}' > $destination_path$RL/$year
		
		# Normalize Year Data, (e.g. Instead of going from 2000 to 2024, from 0 to 23.) using a tmp file 
		awk -v minyear=$minyear '{print $1" "$2" "$3-minyear-1}' $destination_path$RL/$year > tmp
		cat tmp > $destination_path$RL/$year
		
		rm tmp
	done	

done
