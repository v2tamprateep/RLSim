#!/bin/bash

while [[ $# > 1 ]]; do
	key="$1"

	case $key in
	    -s|--sarsa)
	    agent="$2"
	    shift # past argument
	    ;;
	    -q|--qlearning)
	    agent="$2"
	    shift # past argument
	    ;;
	    *)
	            # unknown option
	    ;;
	esac
	shift # past argument or value
done

maze="hexShort"
folder="data/"

for l in `seq 1 4`; do

	if [ "$l" == "1" ]; then
		folder="data/"$agent"_std"
		out=$agent"_std.csv"
	elif [ "$l" == "2" ]; then
		folder="data/"$agent"_RD"
		out=$agent"_RD.csv"
	elif [ "$l" == "3" ]; then
		folder="data/"$agent"_ER"
		out=$agent"_ER.csv"
	elif [ "$l" == "4" ]; then
		folder="data/"$agent"_RDER"
		out=$agent"_RDER.csv"
	fi

	mkdir $folder

	for a in 1; do
		for e in `seq 0.0 0.1 0.0`; do
			for r in `seq 1 1 2`; do
				for b in `seq 1 1 2`; do
					directory="a$a-e$e-r$r-b$b"
					if [ ! -d "${directory//.}" ]; then
						mkdir $folder/${directory//.}
					fi
					python main.py --maze=$maze --agent=$agent --output=$folder/${directory//.}/ -a $a -e $e -r $r -b $b --learning=$l
				done
			done
		done
	done

	python data/compare_path.py --data=$folder/ -a -e -r -b --output=data/$out
	zip -r $folder.zip $folder
	rm -r $folder

	mail -s "UPDATE: $agent $l complete" v2tamprateep@gmail.com < /dev/null
done
