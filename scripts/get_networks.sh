input_path="TFM2/S2_Workspace/dataset/paper_list"
script_path="TFM2/S2_Workspace/scripts"
for file in `ls $input_path`
do
python3 $script_path/get_dyn_net.py "${file%.*}"
done
 
