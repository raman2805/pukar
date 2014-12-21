#!/bin/bash
scripts_dir=`dirname $0`
scripts_dir=`readlink -f $scripts_dir`
data_dir=`readlink -f $scripts_dir/../`

$data_dir/scripts/munge_stations.sh $data_dir/raw/stations.csv $data_dir/munged/stations.csv
