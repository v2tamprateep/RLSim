#!/bin/bash

while [[ $# > 1 ]]; do
    key="$1"

    case $key in
        -a|--algo)
        algo="$2"
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
        -t|--trials)
        trials="$2"
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
        folder=$algo"_std"$reset
        out=$algo"_std"$reset".csv"
    elif [ "$l" == "2" ]; then
        folder=$algo"_RD"$reset
        out=$algo"_RD"$reset".csv"
    elif [ "$l" == "3" ]; then
        folder=$algo"_ER"$reset
        out=$algo"_ER"$reset".csv"
    elif [ "$l" == "4" ]; then
        folder=$algo"_RDER"$reset
        out=$algo"_RDER"$reset".csv"
    fi

    mkdir $folder

    for a in `seq 0.1 0.1 1`; do
        for e in 0; do
            for r in `seq 1 1 10`; do
                for b in `seq 1 1 10`; do
                    directory="a$a-e$e-r$r-b$b"
                    if [ ! -d "${directory//.}" ]; then
                        mkdir $folder/${directory//.}
                    fi
                    python main.py --algo $algo --output $folder/${directory//.}/ -a $a -e $e -r $r -b $b -l $l -r $reset
                                    --mazes maze_set3/unbias maze_set3/unbias maze_set3/antibiasL \
                                    maze_set3/antibiasL maze_set3/antibiasL maze_set3/unbias maze_set3/unbias \
                                    --trials 100 117 62 133 109 142 100
                done
            done
        done
    done

    # python data/compare_path.py --data=$folder/ -a -e -r -b --output=data/$out
    zip -q -r $folder.zip $folder
    rm -r $folder
done

mail -s "UPDATE: $(hostname) complete" v2tamprateep@gmail.com < /dev/null

