#!/bin/bash

agent="sarsa"
maze="hexShort"

for l in `seq 1 4`; do
	folder="/tmp/tempura/"

	if [ "$l" == "1" ]; then
		folder=$folder"sarsa_std"
	elif [ "$l" == "2" ]; then
		folder=$folder"sarsa_RD"
	elif [ "$l" == "3" ]; then
		folder=$folder"sarsa_ER"
	elif [ "$l" == "4" ]; then
		folder=$folder"sarsa_RDER"
	fi

	mkdir $folder

	for a in `seq 0.1 0.1 1`; do
		for e in `seq 0.0 0.1 0.9`; do
			for r in `seq 1 1 10`; do
				for b in `seq 1 1 10`; do
					directory="a$a-e$e-r$r-b$b"
					if [ ! -d "${directory//.}" ]; then
						mkdir $folder/${directory//.}
					fi
					python main.py --maze=$maze --agent=$agent --output=$folder/${directory//.}/ -a $a -e $e -r $r -b $b --learning=$l
				done
			done
		done
	done
	zip -r $folder.zip $folder
	rm -r $folder
	df -h status.txt
	mail -s "$agent $l script complete" v2tamprateep@gmail.com < status.txt
done
