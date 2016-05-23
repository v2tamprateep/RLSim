#!\bin\bash
for i in `seq 1 100`; do python main.py --maze=$maze --agent=$agent --output=../data -a 0.2 -e 0 -r 4 -b 10; done