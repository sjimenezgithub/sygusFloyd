import sys
from z3 import DeclareSort, BoolSort, Function, TransitiveClosure, Solver, Consts, Not

def main():

	# Predicates
	A = DeclareSort("A")
	B = BoolSort()
	R = Function('LINKED', A, A, B)

	# Objects
	graph_size = 400
	str_consts=""
	for c in range(graph_size*graph_size):
		str_consts=str_consts+"c"+str(c)+" "
	str_consts=str_consts+";"
	str_consts=str_consts.replace(" ;","")
	c = Consts(str_consts, A)	

	# Initial State
	s = Solver()		
	for i in range(graph_size):
		for j in range(graph_size):
			index1 = i*graph_size + j
			if(j<graph_size-1):
				index2 = i*graph_size + j + 1
				s.add(R(c[index1], c[index2]))
				s.add(R(c[index2], c[index1]))				
			if(i<graph_size-1):
				index2 = (i+1)*graph_size + j
				s.add(R(c[index1], c[index2]))
				s.add(R(c[index2], c[index1]))

	# Goal State
	TC_R = TransitiveClosure(R)	
	s.add(Not(TC_R(c[0], c[graph_size*graph_size-1])))
	print(s.check())
	sys.exit()	

if __name__ == "__main__":
	main()
