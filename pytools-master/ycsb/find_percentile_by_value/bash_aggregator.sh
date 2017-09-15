#!/bin/bash

# Search for .ycsb files in the SEARCH_DIR, print only folder paths and
# filter out duplicate entries.
subdirs=`find $SEARCH_DIR -name *.ycsb -printf "%h\n" | sort -u`
echo "Founde subdirectories with ycsb files: "$subdirs

function _process_individual_folders_with_ycsb_files {
	echo "---------Processing File ------:  "$1
	echo "---------Additional Arguments--:  "$2

	cd $THIS_DIR/$1
	find_percentile_by_value.py --src_files ./*.ycsb --out_data_file percentiles.slo  $2

}

function merge_subdir_results_into_one_file {
	echo "" > $THIS_DIR/$CURVE
	cd $THIS_DIR/$SEARCH_DIR
	find -name  percentiles.slo | xargs cat >> $THIS_DIR/$CURVE
}


function process_individual_folders_with_ycsb_files {
	ARGS="$1"
	for d in ${subdirs[@]}
	do
		_process_individual_folders_with_ycsb_files $d "$ARGS"
	done
}

function merge_multiple_subdir_results_into_one_file {
	echo "--------- " $THIS_DIR/$CURVE

	for d in ${dirs[@]}
	do
		merge_subdir_results_into_one_file $d
	done
}