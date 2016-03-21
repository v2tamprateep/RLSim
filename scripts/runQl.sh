
#!/bin/bash

agent="qlearning"
maze="hexShort"
folder="../Data/hexShort/ql_path/ql_RD_ae"

for a in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
	for e in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9; do
		directory="a$a-e$e"
		if [ ! -d "${directory//.}" ]; then
			mkdir $folder/${directory//.}
		fi
		python main.py --maze=$maze --agent=$agent --trials=114 --samples=30 -a $a -e $e --consoleOut-Off --output=$folder/${directory//.}/ --fileOut-Off
	done
done

echo "Script Complete"
