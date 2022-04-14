#!/usr/bin/env python
import sys
import random
import argparse

#*****************#
# Functions declarations
#*****************#

def generate_cvc_problem(name,nblocks):
    str_out = ""

    str_out += ";;\n"
    str_out += ";; Blocksword planning domain theory\n"
    str_out += ";;\n"
    str_out += "(set-logic ALL)\n"
    str_out += "(set-option :produce-models true)\n"
    str_out += "\n"
    str_out += ";;; Auxiliary functions\n"
    str_out += "(define-fun getBitAt1D ((bvector (_ BitVec "+str(nblocks)+")) (x Int)) Bool\n"
    for i in range(nblocks):
        str_aux ="0"*nblocks
        string_list = list(str_aux)
        string_list[nblocks-i-1]="1"
        str_aux = "#b"+"".join(string_list)
        str_out += "(ite (= x "+str(i)+") (= (bvand bvector " + str_aux + ") " + str_aux+ ")\n"
    str_out += "false)"+nblocks*")"+"\n"
    str_out += "\n"    

    str_out += "(define-fun setBitAt1D ((bvector (_ BitVec "+str(nblocks)+")) (x Int)) (_ BitVec "+str(nblocks)+")\n"
    for i in range(nblocks):    
        str_aux ="0"*nblocks
        string_list = list(str_aux)
        string_list[nblocks-i-1]="1"
        str_aux = "#b"+"".join(string_list)
        str_out += "(ite (= x "+str(i)+") (bvor bvector "+ str_aux+ ")\n"
    str_out += "bvector)"+nblocks*")"+"\n"
    str_out += "\n"    

    str_out += "(define-fun unsetBitAt1D ((bvector (_ BitVec "+str(nblocks)+")) (x Int)) (_ BitVec "+str(nblocks)+")\n"
    for i in range(nblocks):
        str_aux ="1"*nblocks
        string_list = list(str_aux)
        string_list[nblocks-i-1]="0"
        str_aux = "#b"+"".join(string_list)
        str_out += "(ite (= x "+str(i)+") (bvand bvector "+ str_aux+ ")\n"
    str_out += "bvector)"+nblocks*")"+"\n"
    str_out += "\n"   
    str_out += "(define-fun getBitAt2D ((bvector (_ BitVec "+str(nblocks*nblocks)+")) (x Int) (y Int)) Bool\n"
    for i in range(nblocks):
        str_out += "(ite (= x "+str(i)+")\n"
        for j in range(nblocks):
            str_aux ="0"*nblocks*nblocks
            string_list = list(str_aux)
            string_list[nblocks*nblocks-(i*nblocks+j)-1]="1"
            str_aux = "#b"+"".join(string_list)
            str_out += "(ite (= y "+str(j)+") (= (bvand bvector "+ str_aux+ ") "+ str_aux+ ")\n"
        str_out += "false"+nblocks*")"+"\n"
    str_out += "false)"+nblocks*")"+"\n"
    str_out += "\n"   

    str_out += "(define-fun setBitAt2D ((bvector (_ BitVec "+str(nblocks*nblocks)+")) (x Int) (y Int)) (_ BitVec "+str(nblocks*nblocks)+")\n"
    for i in range(nblocks):
        str_out += "(ite (= x "+str(i)+")\n"
        for j in range(nblocks):
            str_aux ="0"*nblocks*nblocks
            string_list = list(str_aux)
            string_list[nblocks*nblocks-(i*nblocks+j)-1]="1"
            str_aux = "#b"+"".join(string_list)
            str_out += "(ite (= y "+str(j)+")  (bvor bvector "+str_aux+")\n"   
        str_out += "bvector"+nblocks*")"+"\n"
    str_out += "bvector)"+nblocks*")"+"\n"
    str_out += "\n"   

    str_out += " (define-fun unsetBitAt2D ((bvector (_ BitVec "+str(nblocks*nblocks)+")) (x Int) (y Int)) (_ BitVec "+str(nblocks*nblocks)+")\n"  
    for i in range(nblocks):
        str_out += "(ite (= x "+str(i)+")\n"
        for j in range(nblocks):
            str_aux ="1"*nblocks*nblocks
            string_list = list(str_aux)
            string_list[nblocks*nblocks-(i*nblocks+j)-1]="0"
            str_aux = "#b"+"".join(string_list)
            str_out += "(ite (= y "+str(j)+")  (bvand bvector "+str_aux+")\n"   
        str_out += "bvector"+nblocks*")"+"\n"
    str_out += "bvector)"+nblocks*")"+"\n"
    str_out += "\n"   

    str_out += ";;;\n"
    str_out += ";; Structure of the Blocksword states\n" 
    str_out += "(declare-datatypes ((PlanningState 0))\n"
    str_out += "   (((rec (handempty Bool)\n" 
    str_out += "          (holding (_ BitVec "+str(nblocks)+"))\n"
    str_out += "          (clear (_ BitVec "+str(nblocks)+"))\n"
    str_out += "          (ontable (_ BitVec "+str(nblocks)+"))\n"
    str_out += "          (on (_ BitVec "+str(nblocks*nblocks)+"))))))\n"
    str_out += "\n"
    str_out += ";;;\n"
    str_out += ";; The Blocksword action schemes\n"
    str_out += "(define-fun putdown ((s PlanningState) (x Int)) PlanningState\n"
    str_out += "(ite (and (getBitAt1D (holding s) x))\n"
    str_out += "      (rec \n"
    str_out += "           true\n"
    str_out += "           (unsetBitAt1D (holding s) x)\n"
    str_out += "           (setBitAt1D (clear s) x)  \n"
    str_out += "           (setBitAt1D (ontable s) x)  \n"
    str_out += "           (on s))\n"
    str_out += "      s))\n"
    str_out += "\n"    
    str_out += "(define-fun pickup ((s PlanningState) (x Int)) PlanningState\n"
    str_out += " (ite (and (handempty s)\n"
    str_out += "           (getBitAt1D (ontable s) x)\n"
    str_out += "           (getBitAt1D (clear s) x))\n"
    str_out += "      (rec false\n"
    str_out += "           (setBitAt1D (holding s) x)\n"
    str_out += "           (unsetBitAt1D (clear s) x)\n"  
    str_out += "           (unsetBitAt1D (ontable s) x)\n"  
    str_out += "           (on s))\n"
    str_out += "      s))\n"
    str_out += "\n"    
    str_out += "(define-fun unstack ((s PlanningState) (x Int) (y Int)) PlanningState\n"
    str_out += "  (ite (and (handempty s) \n"
    str_out += "            (getBitAt1D (clear s) x)\n"
    str_out += "            (getBitAt2D (on s) x y))\n"
    str_out += "       (rec false \n"
    str_out += "            (setBitAt1D (holding s) x)\n"
    str_out += "            (setBitAt1D (unsetBitAt1D (clear s) x) y)\n"
    str_out += "            (ontable s)\n"
    str_out += "            (unsetBitAt2D (on s) x y))\n"
    str_out += "       s))\n"
    str_out += "\n"    
    str_out += "(define-fun stack ((s PlanningState) (x Int) (y Int)) PlanningState\n"
    str_out += "  (ite (and (getBitAt1D (holding s) x)\n"
    str_out += "            (getBitAt1D (clear s) y)\n"            
    str_out += "            )\n"
    str_out += "       (rec true\n"
    str_out += "            (unsetBitAt1D (holding s) x)\n"
    str_out += "            (unsetBitAt1D (setBitAt1D (clear s) x) y)\n"
    str_out += "            (ontable s)\n"
    str_out += "            (setBitAt2D (on s) x y))\n"
    str_out += "        s))\n"
    str_out += "\n"    
    str_out += ";;; syntactic constraints\n"
    str_out += "(synth-fun plan ((s PlanningState)) PlanningState\n"
    str_out += "((Start PlanningState) (SN PlanningState) (I1 Int ) (I2 Int ))\n"
    str_out += "((Start PlanningState (SN))\n"
    str_out += " (SN PlanningState (s (pickup SN I1) (putdown SN I1) (stack SN I1 I2) (unstack SN I1 I2)))\n"
    str_out += " (I1 Int ("+str(list(range(nblocks))).replace(","," ").replace("[","").replace("]","")+"))\n"
    str_out += " (I2 Int ("+str(list(range(nblocks))).replace(","," ").replace("[","").replace("]","")+"))))\n"

    str_out += "\n"
    str_out += ";;; Initial state and goals\n"
    str_aux = nblocks*nblocks*"0"
    for i in range(nblocks-1):
        j=i+1
        string_list = list(str_aux)        
        string_list[nblocks*nblocks-(i*nblocks+j)-1]="1"
        str_aux = "".join(string_list)
    str_out += "(constraint (= (rec true #b" +nblocks*"0" +" #b" +nblocks*"1" +" #b" + nblocks*"1" + " #b" + nblocks*nblocks*"0"+") (plan (rec true #b"+nblocks*"0"+" #b" + (nblocks-1)*"0" +"1 #b1"+(nblocks-1)*"0"+" #b"+str_aux+"))))\n"
    str_out += "\n"
    str_out += " (check-synth)\n"    


    return str_out
#*****************#



#*****************#
# MAIN
#*****************#
# Reading the command line arguments

def main():
    parser = argparse.ArgumentParser(description="Blocks Ontable generator")
    parser.add_argument("-f", "--from_nth", type=int, required=True)
    parser.add_argument("-t", "--to_nth", type=int, required=True)
    parser.add_argument("-s", "--step", type=int, nargs='?', default=1, required=False)
    parser.add_argument("-o", "--out_folder", type=str, required=True)
    args = parser.parse_args()

    from_nth = args.from_nth
    to_nth = args.to_nth
    step = args.step
    out_folder = args.out_folder

    if step < 1 or to_nth < from_nth:
        sys.exit(-2)

    # GENERATION
    vblocks = range(from_nth, to_nth+1)

    # INSTANCES
    random.seed(1007)

    num_of_same_complexity_problems = 1
    for i in range(from_nth,to_nth+1,step):
        for j in range( num_of_same_complexity_problems ) :
            # Problem name
            problem_name = "BLOCKS-" + str( (i+step-from_nth)//step )

            str_problem = generate_cvc_problem(problem_name,vblocks[i-from_nth])

            f_problem = open( out_folder + str( (i+step-from_nth)//step ) + "-" + str( j ) + ".sl","w")
            f_problem.write( str_problem )
            f_problem.close()
    sys.exit(0)


if __name__ == "__main__":
    main()



