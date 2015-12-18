
#!/bin/bash

agent="qlearning"

for a in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
	for g in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
		for e in 1.0; do
			python main.py --maze=mapped --agent=$agent --trials=114 --sampleSize=60 -a $a -g $g -e $e --consoleOut-Off --output=../researchData/mapped/$agent/
		done
	done
done

echo "Script Complete"