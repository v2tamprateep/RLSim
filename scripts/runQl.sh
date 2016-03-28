
#!/bin/bash

agent="sarsa"
maze="hexShort"
folder="../Data/hexShort/sarsa_path/sarsa_RDER_arb"

# alpha
for a in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
	# reward
	for r in 1 2 3 4 5 6 7 8 9 10; do
		# back cost 
		for b in 1 2 3 4 5 6 7 8 9 10; do
			echo -e "agent: $agent\nmaze: $maze\nalpha: $a\nreward: $r\nback cost: $b" > README.txt
			directory="a$a-r$r-b$b"
			if [ ! -d "${directory//.}" ]; then
				mkdir $folder/${directory//.}
			fi
			python main.py --maze=$maze --agent=$agent --output=$folder/${directory//.}/ -a $a --reward=$r --back_cost=$b
		done
	done
done

echo "Script Complete"
