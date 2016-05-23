
#!/bin/bash

agent="sarsa"
maze="hexShort"
folder="../Data/hexShort/reset_arb/sarsa_ER"

mkdir $folder
echo "sarsa"
# alpha
for a in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
	# reward
	for r in 1 2 3 4 5 6 7 8 9 10; do
		# back cost 
		for b in 1 2 3 4 5 6 7 8 9 10; do
			directory="a$a-r$r-b$b"
			if [ ! -d "${directory//.}" ]; then
				mkdir $folder/${directory//.}
			fi
			python main.py --maze=$maze --agent=$agent --output=$folder/${directory//.}/ -a $a -e 0 -r $r -b $b --learning=3
		done
	done
done

agent="qlearning"
maze="hexShort"
folder="../Data/hexShort/reset_arb/ql_ER"

mkdir $folder
echo "qlearning"
# alpha
for a in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
	# reward
	for r in 1 2 3 4 5 6 7 8 9 10; do
		# back cost 
		for b in 1 2 3 4 5 6 7 8 9 10; do
			directory="a$a-r$r-b$b"
			if [ ! -d "${directory//.}" ]; then
				mkdir $folder/${directory//.}
			fi
			python main.py --maze=$maze --agent=$agent --output=$folder/${directory//.}/ -a $a -e 0 -r $r -b $b --learning=3
		done
	done
done

# folder="../Data/hexShort/reset_arb/sarsa_RDER"

# mkdir $folder

# # alpha
# for a in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do
# 	# reward
# 	for r in 1 2 3 4 5 6 7 8 9 10; do
# 		# back cost 
# 		for b in 1 2 3 4 5 6 7 8 9 10; do
# 			directory="a$a-r$r-b$b"
# 			if [ ! -d "${directory//.}" ]; then
# 				mkdir $folder/${directory//.}
# 			fi
# 			python main.py --maze=$maze --agent=$agent --output=$folder/${directory//.}/ -a $a -e 0 -r $r -b $b --learning=4
# 		done
# 	done
# done
