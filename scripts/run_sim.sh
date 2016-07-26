#!/bin/bash

while [[ $# > 1 ]]; do
    key="$1"

    case $key in
        -A|--agent)
        agent="$2"
        shift # past argument
        ;;
        -r|--reset)
        reset="$2"
        shift # past argument
        ;;
        -a|--alpha)
        a="$2"
        shift # past argument
        ;;
        -e|--epsilon)
        e="$2"
        shift # past argument
        ;;
        -b|--back)
        b="$2"
        shift # past argument
        ;;
        -R|--reward)
        R="$2"
        shift # past argument
        ;;
        -l|--learning)
        l="$2"
        shift # past argument
        ;;
        -f|--folder)
        folder="$2"
        shift # past argument
        ;;
        *)
                # unknown option
        ;;
    esac
    shift # past argument or value
done

maze="hexShort"

if [ "$l" == "1" ]; then
    folder=$folder$agent"_std"$reset
elif [ "$l" == "2" ]; then
    folder=$folder$agent"_RD"$reset
elif [ "$l" == "3" ]; then
    folder=$folder$agent"_ER"$reset
elif [ "$l" == "4" ]; then
    folder=$folder$agent"_RDER"$reset
fi

mkdir $folder
for d in `seq 1 1 10`; do
    for e in `seq 0.0 0.1 0.9`; do
        directory="a$a-e$e-r$R-b$b-d$d"
        if [ ! -d "${directory//.}" ]; then
            mkdir $folder/${directory//.}
        fi
        python main.py --maze=$maze --agent=$agent --output=$folder/${directory//.}/ -a $a -e $e -r $R -b $b -d $d --learning=$l --Qreset=$reset
    done
done
