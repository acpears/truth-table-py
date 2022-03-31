import re
import os

 # double negation and 
#checks if v is in the variables that are defined
def isVar(v,var):
    # s = removeNot(v)[0]
    if v in var or v == 't' or v == 'f':
        return True
    return False

# def removeNot(str):
#     s = str
#     count = 0;
#     while(len(s) >= 1):
#         if(s[0] != '~'):
#             break
#         count += 1;
#         s = s.removeprefix("~")
#     return (s,count)

#method to peek at first element of list
def peek(list):
    if list:
        return list[0] # this will get the last element of stack
    else:
        return None

#method to determine which operator with the most precedence
def precedence(a,b):
    if(a == "and"):
        return True
    elif(a == "or"):
        return b != "and"
    elif(a == "imply" or a == "xnor"):
        return not (b != 'or' or b != 'and')
    else:
        return False

def expressionParse(var,exp):
    splitStr = re.split('(?<=\()|(?=\()|(?<=\))|(?=\))|(?<=\~)|(?=\~)|\s',exp)
    #print(splitStr)

    #lists to store operands and operators while we loop through elements of expression
    operators = []
    result = []

    opCount = 0
    varCount = 0
    brackBal = 0

    #infix to suffix algorithm
    for s in splitStr:
        s = s.lower()
        if s == "": continue #ignore empty element due to split
        if isVar(s,var):
            result.append(s)
            varCount += 1
        else:
            if s == 'and' or s == 'or' or s == 'imply' or s == 'xnor':
                if len(operators) == 0:
                    operators.insert(0,s)
                else:
                    while len(operators) != 0 and precedence(peek(operators),s):
                        el = operators.pop(0)
                        result.append(el)
                        if(el != '~'):
                            opCount += 1;
                    while len(operators) != 0 and peek(operators) == '~':
                        result.append(operators.pop(0))
                    operators.insert(0,s)
            elif s == '(':
                brackBal += 1
                operators.insert(0,s)
            elif s == ')':
                if(brackBal <= 0): return None
                brackBal -= 1
                while peek(operators) != '(':
                    el = operators.pop(0)
                    result.append(el)
                    if(el != '~'):
                        opCount += 1;
                operators.pop(0)
            elif s == '~':
                operators.insert(0,s)
            else:
                return None
    while(len(operators) != 0):
        el = operators.pop(0);
        result.append(el)
        if(el != '~'):
            opCount += 1;

    #Check to make sure the right number of vars, operators and parenthese in equation
    if(varCount-1 != opCount or brackBal != 0):
        return None
    return result

def expressionEval(var, exp):
    vars = []
    for s in exp:
        if isVar(s,var):
            if(s == 't'):
                vars.insert(0,True)
            elif(s == 'f'):
                vars.insert(0,False)
            else: 
                vars.insert(0,var.get(s))
        elif s == 'and':
            var2 = vars.pop(0)
            var1 = vars.pop(0)
            r = var1 and var2
            vars.insert(0,r) 
        elif s == 'or':
            var2 = vars.pop(0)
            var1 = vars.pop(0)
            r = var1 or var2
            vars.insert(0,r) 
        elif s == 'imply':
            var2 = vars.pop(0)
            var1 = vars.pop(0)
            r = (not var1) or var2
            vars.insert(0,r) 
        elif s == 'xnor':
            var2 = vars.pop(0)
            var1 = vars.pop(0)
            r = (var1 and var2) or ((not var1) and (not var2))
            vars.insert(0,r) 
        elif s == '~':
            var1 = vars.pop(0)
            r = not var1
            vars.insert(0,r)
    return vars.pop();

#Returns table of boolean combination for n variables
def bool_combs(n):
    if not n:
        return [[]]
    result = []
    for comb in bool_combs(n-1):
        result.append(comb + [True])
        result.append(comb + [False])
    return result

#Returns table of all boolean combinations for our variables
def truth_table(var):
    truthTbl = []
    numVar = len(var)
    bool_vals = bool_combs(numVar)
    for i in range(len(bool_vals)):
        truthTbl.insert(i,{})
        for j in range(numVar):
            truthTbl[i][var[j]] = bool_vals[i][j];
    return truthTbl

def expressionTruthTableEval(tbl, exp):
    fCount = 0
    tCount = 0
    result = []
    for el in tbl:
        temp = expressionEval(el,exp)
        result.append(temp)
        if temp:
            tCount += 1
        elif not temp:
            fCount += 1
    type = ""
    if(tCount == 0): type = "contradiction"
    elif(fCount == 0): type = "tautology"
    else: type = "contingency"
    return (result,type)
    
def printTruthTable(tbl, result):
    # Print table headers
    print("")
    for var in tbl[0]:
        print(var, "\t", end = " ")
    print(" | ","S")
    iter = 0
    for el in tbl:
        for i in el:
            print(el[i], "\t", end = " ")
        print(" | " , result[0][iter])
        iter += 1
    # Print whether sentence is a contradiction, tautology or contingency
    print("\nThe propositional sentence S is a", result[1], "\n")


#Main application problem 1
def problem1():
    run = True
    os.system('cls' if os.name == 'nt' else 'clear')
    while(run):
        print("** PROBLEM #1 ***")
        vars = {} #dictionary to hold variables and truth values
        count = 1;
        while(True):
            try:
                iter = int(input("\nInput the number of variables in your sentence: "))
                break
            except:
                print("ERROR... please input number")
                continue
        for i in range(iter):
            while(True):
                var = input("\nPlease input propositional variable #%d: " % count).replace(" ","").lower()
                if var in vars:
                    print("ERROR... variable has already been input")
                    continue
                break
            while(True):
                val = input("Please input variable %s's truth value (T or F): " % var).replace(" ","").lower()
                if(val == "t"):
                    vars[var] = True
                    break
                elif(val == "f"):
                    vars[var] = False
                    break
                else:
                    print("ERROR... please input 'T' or 'F'")
            count += 1
    
        print("\nPlease input your propositional sentence.")
        print("- Your sentence must contain the variables ", end = "")
        for k in vars.keys():
            print("'%s'" % k, end= " ")
        print("or the truth values 'T' and 'F'", end= "")
        print("\n- You can use any of the following operators AND, OR, IMPLY or XNOR.\n- The use of parenthese is permitted.\n- Please make sure that all variables, operators and parentheses are sperated by a space.\n- To negate please use '~' before any variable (no space).")
        while(True):
            exp = input("\nINPUT SENTENCE (S): ").lower()
            expression = expressionParse(vars,exp)
            if(expression == None):
                print("\n*** Error in your sentence. Please try again! ***")
                continue
            result = expressionEval(vars, expression)
            print("OUTPUT: ",result)
            break;
        while(True):
            cont = input("\nWould you like to input new variables and sentence? (Y or N): ").lower()
            if cont == 'y': break
            elif cont == 'n': 
                run = False;
                break;
        os.system('cls' if os.name == 'nt' else 'clear')

#Main application problem 2
def problem2():
    os.system('cls' if os.name == 'nt' else 'clear')
    run = True;
    while(run):
        print("** PROBLEM #2 ***")
        numVars = 0
        count = 1;
        vars = []
        tTable = []
        while(True):
            try:
                iter = int(input("\nInput the number of variables in your sentence: "))
                break
            except:
                print("ERROR... please input number")
                continue
        for i in range(iter):
            while(True):
                var = input("\nPlease input propositional variable #%d: " % count).replace(" ","").lower()
                if var in vars:
                    print("ERROR... variable has already been input")
                    continue
                break
            vars.append(var)
            count += 1
        tTable = truth_table(vars)
        print("\nPlease input your propositional sentence.")
        print("- Your sentence must contain the variables ", end = "")
        for k in vars:
            print("'%s'" % k, end= " ")
        print("or the truth values 'T' and 'F'", end= "")
        print("\n- You can use any of the following operators AND, OR, IMPLY or XNOR.\n- The use of parenthese is permitted.\n- Please make sure that all variables, operators and parentheses are sperated by a space.\n- To negate please use '~' before any variable (no space).")
        while(True):
            exp = input("\nINPUT SENTENCE (S): ").lower()
            expression = expressionParse(vars,exp)
            if(expression == None):
                print("\n*** Error in your sentence. Please try again! ***")
                continue
            result = expressionTruthTableEval(tTable,expression)
            printTruthTable(tTable,result)
            break
        while(True):
            cont = input("Would you like to input new variables and sentence? (Y or N): ").lower()
            if cont == 'y': break
            elif cont == 'n': 
                run = False;
                break;
        os.system('cls' if os.name == 'nt' else 'clear')


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("PROGRAMMING ASSIGNMENT #2 - COMP5361\n")
    while(True):
        str1 = input("\nWhat problem would you like to run ('1', '2' or 'exit'): ").replace(" ", "")
        if(str1 == "1"):
            problem1()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif(str1 == "2"):
            problem2()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif(str1 == "exit"):
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        else:
            print("ERROR... please input either '1', '2' or 'exit")


if __name__=="__main__":
    main()

# exp = "~y AND x"
# splitStr = re.split('(?<=\()|(?=\()|(?<=\))|(?=\))|(?<=\~)|(?=\~)|\s',exp)
# print(splitStr)