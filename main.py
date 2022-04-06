from z3 import DeclareSort, BoolSort, Function, TransitiveClosure, Solver, Consts, Not


def main():
	A = DeclareSort("A")
	B = BoolSort()
	R = Function('R', A, A, B)
	TC_R = TransitiveClosure(R)
	s = Solver()
	a, b, c = Consts('a b c', A)
	s.add(R(a, b))
	s.add(R(b, c))
	#s.add(Not(TC_R(a, c)))  # a not connected to c produces unsat
	s.add(TC_R(a, c))  # a connected to c produces sat
	print(s.check())  
	# m = s.model() 
	# print(m)
	# m.eval(...)  # Evaluate the model on an arbitrary expression
	

if __name__ == "__main__":
	main()
