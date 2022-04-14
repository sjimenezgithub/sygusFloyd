import os, sys, time, resource, glob

def main():
	registers=[]

	file = open('registers.txt', 'w')
	file.close()	

	for fname in sorted(glob.glob("./tmp/*.sl")):
		str_cmd="ulimit -t 1000; ~/software/cvc/cvc5-Linux " + fname + " > " + fname+ ".log"
		print("Executing..." + str_cmd)

		time_start = time.perf_counter()
		os.system(str_cmd)
		time_elapsed = (time.perf_counter() - time_start)

		reg = fname+ " %5.1f secs" % (time_elapsed)
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

