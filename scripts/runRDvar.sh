
#!/bin/bash

agent="sarsa"
maze="hexShort"
folder="../Data/hexShort/sarsa_path/sarsa_RDER_er"

for r in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
	for e in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
		directory="e$e-r$r"
		if [ ! -d "${directory//.}" ]; then
			mkdir $folder/${directory//.}
		fi
		python main.py --maze=$maze --agent=$agent --trials=114 --samples=30 -e $e -r $r --consoleOut-Off --output=$folder/${directory//.}/ --fileOut-Off 
	done
done

echo "Script Complete"
