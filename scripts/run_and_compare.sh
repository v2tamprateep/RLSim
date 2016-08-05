#!/bin/bash

while [[ $# > 1 ]]; do
	key="$1"

	case $key in
	    -a|--agent)
	    agent="$2"
	    shift # past argument
	    ;;
	    -r|--reset)
	    reset="$2"
	    shift # past argument
	    ;;
	    -m|--maze)
	    maze="$2"
	    shift
	    ;;
	    *)
	            # unknown option
	    ;;
	esac
	shift # past argument or value
done

for l in `seq 1 4`; do

	if [ "$l" == "1" ]; then
		folder=$agent"_std"$reset
		out=$agent"_std"$reset".csv"
	elif [ "$l" == "2" ]; then
		folder=$agent"_RD"$reset
		out=$agent"_RD"$reset".csv"
	elif [ "$l" == "3" ]; then
		folder=$agent"_ER"$reset
		out=$agent"_ER"$reset".csv"
	elif [ "$l" == "4" ]; then
		folder=$agent"_RDER"$reset
		out=$agent"_RDER"$reset".csv"
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
					python main.py --maze=$maze --agent=$agent --output=$folder/${directory//.}/ -a $a -e $e -r $r -b $b --learning=$l --Qreset=$reset
				done
			done
		done
	done

	# python data/compare_path.py --data=$folder/ -a -e -r -b --output=data/$out
	zip -r $folder.zip $folder
	rm -r $folder
done

mail -s "UPDATE: $(hostname) complete" v2tamprateep@gmail.com < /dev/null

