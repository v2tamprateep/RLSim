
#!/bin/bash

agent="qlearning"
maze="hexShort"
folder="../Data/hexShort/epsilon_optimal/sample60_2"

# alpha
# for a in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
for a in 0.0; do
	for e in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
	# reward
	# for r in 1 2 3 4 5 6 7 8 9 10; do
		# back cost 
		# for b in 1 2 3 4 5 6 7 8 9 10; do
			echo -e "agent: $agent\nmaze: $maze\nalpha: $a\nepsilon: $e\nreward: $r\nback cost: $b" > README.txt
			directory="a$a-e$e"
			if [ ! -d "${directory//.}" ]; then
				mkdir $folder/${directory//.}
			fi
			python main.py --maze=$maze --agent=$agent --output=$folder/${directory//.}/ -a $a -e $e --samples=60
		# done
	done
done

echo "Script Complete"
