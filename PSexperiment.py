import os, sys, time, resource

def main():
	registers=[]

	file = open('registers.txt', 'w')
	file.close()	

	for i in range(1,9):
		fname="cadenas" + str(i) 
		str_cmd="ulimit -t 600; ~/software/cvc/cvc5-Linux " + fname + ".sl > " + fname+ ".log"
		print("Executing..." + str_cmd)

		time_start = time.perf_counter()
		os.system(str_cmd)
		time_elapsed = (time.perf_counter() - time_start)

		reg = str(i)+ " %5.1f secs" % (time_elapsed)
		registers.append(reg)
		file = open('registers.txt', 'a')
		file.write(reg+"\n")
		file.close()	

	print("----------------------------------------")
	for r in registers:
		print(r)	

	sys.exit()

if __name__ == "__main__":
	main()