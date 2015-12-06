#!/bin/bash

# output="~/RLSim/Data/comparison_Results/mappedVSmice"
output="./out"
fileA="Data/mouseData"
folder="mapped"

echo "Compare contents of $fileBfolder against $fileA" >> $output

for data in Data/$folder/qlearning-a0.0-g0.0-e0.5; do
	printf "$data: " >> $output
	python scripts/compare.py --fileA=$fileA --fileB=$data >> $output
	echo >> $output
done

echo "Script complete"
