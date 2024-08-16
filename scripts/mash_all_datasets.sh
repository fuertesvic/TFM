input_path="TFM2/xgboost/data"
out_path="TFM2/xgboost"
for RL in `ls $input_path`
do 
	input_file=$input_path/$RL
	awk -v rl="$RL" '{print rl, $0}' $input_file  > tmp
	cat tmp >> $out_path/macro_file
	rm tmp
done

