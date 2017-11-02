# Converts simple BASIC into Verilog
# Additions and Modifications (c) Richard P. Martin, October 2017 

# This file provides the runtime support for running a basic program
# Assumes the program has been parsed using basparse.py

# built on PLY (Python L(ex Yacc) code from David M. Beazley dave@dabeaz.com

import sys
import math
import random
import numpy as np
import argparse

# This object is a statement in the Programming Language
# statement in the PL get reduced into data-flow nodes and control nodes in the verilog
# each verilog node reponds to a set of control inputs at each clock cycle

class StatementNode:

    def __init__(self, index, lineno,type,instr):
        self.index = index        # which statement this is in lexical order
        self.name = str(lineno)   # unique ID for this statement node in the graph as a string 
        self.lineno = lineno      # the line number in the program 
        self.type = type          # the type Eg FOR, LET, OOTO 
        self.instr = instr        # parsed text of the statement as a list of lists
        self.control_nodes = []        # a list of control nodes 
        self.successors = []      # the statements that could follow
        self.successors_taken = []  # for NEXT and IF statements - following statement if the condition is true 
        self.predecessors = []        # statements that could come before this one
        self.predecessors_taken = []  # taken ifs and nexts that could come before this one 
        self.read_vars = []          # variables that are read by this statement 
        self.write_vars = []         # variables that are written to by this statement
        self.gosub_statements = []        # for a return, list of possible gosubs
        self.return_statement = ''   # for a gosub, the matching return statement 
        self.verilog = []  # A list of veriog statements to output for the BASIC statement 
        self.visited = False    # for graph traversal, if visited or not 

    # this comparison code allows us to sort statements by BASIC line number 
    def __lt__(self, other):
        if (other == None): 
            return False 
        else:
            return (self.lineno < other.lineno)

    def __le__(self, other):
        if (other == None):
            return False 
        else: 
            return (self.lineno <= other.lineno)
    
    def __eq__(self, other):
        if (other == None):
            return False
        else: 
            return (self.lineno == other.lineno)
    
    def __ne__(self, other):
        if (other == None):
            return True
        else:
            return (self.lineno != other.lineno)

    def __gt__(self, other):
        if (other == None):
            return True
        else: 
            return (self.lineno > other.lineno)

    def __ge__(self, other):
        if (other == None):
            return True
        else: 
            return (self.lineno >= other.lineno)

# This object is a control node in the Verilog
# 
class ControlNode:
    def __init__(self,type,statement,index, name,lineno):
        self.type = type          # the type Eg 
        self.index = index        # which statement this is in lexical order
        self.name = name          # unique ID for this control node in the graph as a string
        self.lineno = lineno      # basic program line number that generated this node 
        self.statement = statement   # the programming language statement for this control node 
        self.successors = []      # the statements that could follow
        self.successors_taken = []  # for NEXT and IF statements - following statement if the condition is true 
        self.predecessors = []        # statements that could come before this one
        self.predecessors_taken = []  # taken ifs and nexts that could come before this one
        self.gosub_nodes = []        # for a return, the possible gosub sources 
        self.return_targets = []     # for a return, the possible nodes to return to 
        self.read_vars = []    # variables read by the node 
        self.write_vars= []    # vartiable written by the node 
        self.verilog =   []    # verilog to output for this control node
        self.visited = False   # for graph traversal, if visited or not
        
    # this comparison code allows us to sort statements by BASIC line number 
    def __lt__(self, other):
        if (other == None): 
            return False 
        else:
            return (self.name < other.name)

    def __le__(self, other):
        if (other == None):
            return False 
        else: 
            return (self.name <= other.name)
    
    def __eq__(self, other):
        if (other == None):
            return False
        else: 
            return (self.name == other.name)
    
    def __ne__(self, other):
        if (other == None):
            return True
        else:
            return (self.name != other.name)

    def __gt__(self, other):
        if (other == None):
            return True
        else: 
            return (self.name > other.name)

    def __ge__(self, other):
        if (other == None):
            return True
        else: 
            return (self.name >= other.name)

# This is a data node at the verilog level, which corresponds to 
# a variable at the programming language level
# a variable can also be arrays
class Variable:
    def __init__(self, name, dimensions):
        self.name = name
        self.dimensions = dimensions # an array of values for the dimensions. 
        self.write_statements = []   # statements that write to this variable 
        self.read_statements = []    # statements that read from this variable 
        self.write_nodes = []        # list of control nodes that write to this var
        self.read_nodes = []         # list of control nodes read this var
        self.isfifo = False          # is the regular variable or a FIFO
        
    # this code allows us to sort the variables alphanumerically
    def __lt__(self, other):
        if (other == None): 
            return False 
        else:
            return (self.name < other.name)

    def __le__(self, other):
        if (other == None):
            return False 
        else: 
            return (self.name <= other.name)
    
    def __eq__(self, other):
        if (other == None):
            return False
        else: 
            return (self.name == other.name)
    
    def __ne__(self, other):
        if (other == None):
            return True
        else:
            return (self.name != other.name)

    def __gt__(self, other):
        if (other == None):
            return True
        else: 
            return (self.name > other.name)

    def __ge__(self, other):
        if (other == None):
            return True
        else: 
            return (self.name >= other.name)

# hack to transform = to == inside an relational expression 
global inside_relational_expression

        
class BasicInterpreter:

    # Initialize the interpreter. prog is a dictionary
    # containing (line,statement) mappings
    def __init__(self, prog,args):
        self.prog = prog
        self.program_args = args
        self.functions = {           # Built-in function table
            'SIN': lambda z: math.sin(self.eval(z)),
            'COS': lambda z: math.cos(self.eval(z)),
            'TAN': lambda z: math.tan(self.eval(z)),
            'ATN': lambda z: math.atan(self.eval(z)),
            'EXP': lambda z: math.exp(self.eval(z)),
            'ABS': lambda z: abs(self.eval(z)),
            'LOG': lambda z: math.log(self.eval(z)),
            'SQR': lambda z: math.sqrt(self.eval(z)),
            'INT': lambda z: int(self.eval(z)),
            'RND': lambda z: random.random(),
            'TOHEX': lambda z: hex(self.eval(z) & 2**32-1),
            'FROMHEX': lambda z: int(self.eval(z),16)
        }
        self.inside_verilog_str = False
        
    # Collect all data statements
    def collect_data(self):
        self.data = []
        for lineno in self.stat:
            if self.prog[lineno][0] == 'DATA':
                self.data = self.data + self.prog[lineno][1]
        self.dc = 0                  # Initialize the data counter

    # Check for end statements
    def check_end(self):
        has_end = 0
        for lineno in self.stat:
            if self.prog[lineno][0] == 'END' and not has_end:
                has_end = lineno
        if not has_end:
            print("NO END INSTRUCTION")
            self.error = 1
            return
        if has_end != lineno:
            print("END IS NOT LAST")
            self.error = 1

    # Check loops
    def check_loops(self):
        for pc in range(len(self.stat)):
            lineno = self.stat[pc]
            if self.prog[lineno][0] == 'FOR':
                forinst = self.prog[lineno]
                loopvar = forinst[1]
                for i in range(pc + 1, len(self.stat)):
                    if self.prog[self.stat[i]][0] == 'NEXT':
                        nextvar = self.prog[self.stat[i]][1]
                        if nextvar != loopvar:
                            continue
                        self.loopend[pc] = i
                        self.looptarget[i] = pc 
                        break
                else:
                    print("FOR WITHOUT NEXT AT LINE %s" % self.stat[pc])
                    self.error = 1

    # Evaluate an expression
    def eval(self, expr):
        etype = expr[0]
        if etype == 'NUM':
            return expr[1]
        elif etype == 'GROUP':
            return self.eval(expr[1])
        elif etype == 'UNARY':
            if expr[1] == '-':
                return -self.eval(expr[2])
            elif expr[1] == '~':
                return ~self.eval(expr[2])
            elif expr[1] == 'NOT':
                return (not self.eval(expr[2]))
        elif etype == 'BINOP':
            if expr[1] == '+':
                return (self.eval(expr[2])) + (self.eval(expr[3]))
            elif expr[1] == '-':
                return self.eval(expr[2]) - self.eval(expr[3])
            elif expr[1] == '*':
                return self.eval(expr[2]) * self.eval(expr[3])
            elif expr[1] == '/':
                return float(self.eval(expr[2])) / self.eval(expr[3])
            elif expr[1] == '**':
                return abs(self.eval(expr[2]))**self.eval(expr[3])
            elif expr[1] == '<<':
                return self.eval(expr[2]) << self.eval(expr[3])
            elif expr[1] == '>>':
                return self.eval(expr[2]) >> self.eval(expr[3])
            elif expr[1] == '&':
                return self.eval(expr[2]) & self.eval(expr[3])
            elif expr[1] == '|':
                return self.eval(expr[2]) | self.eval(expr[3])
            elif expr[1] == '^':
                return self.eval(expr[2]) ^ self.eval(expr[3])
            elif expr[1] == '%':
                return self.eval(expr[2]) % self.eval(expr[3])
            elif expr[1] == 'AND':
                return self.eval(expr[2]) and self.eval(expr[3])
            elif expr[1] == 'OR':
                return self.eval(expr[2]) or self.eval(expr[3])
            elif expr[1] == '==':
                if self.eval(expr[2]) == self.eval(expr[3]):
                    return 1
                else:
                    return 0 
            else:
                print "UNKNOWN OPERATOR IN EXPRESSION", expr
                return 0
            
        elif etype == 'VAR':
            var, dim1, dim2 = expr[1]
            if not dim1 and not dim2:
                if var in self.vars:
                    return self.vars[var]
                else:
                    print("UNDEFINED VARIABLE %s AT LINE %s" %
                          (var, self.stat[self.pc]))
                    raise RuntimeError
            # May be a list lookup or a function evaluation
            if dim1 and not dim2:
                if var in self.functions:
                    # A function
                    return self.functions[var](dim1)
                else:
                    # A list evaluation
                    if var in self.lists:
                        dim1val = self.eval(dim1)
                        if dim1val < 1 or dim1val > len(self.lists[var]):
                            print("LIST INDEX OUT OF BOUNDS AT LINE %s" %
                                  self.stat[self.pc])
                            raise RuntimeError
                        return self.lists[var][dim1val - 1]
            if dim1 and dim2:
                if var in self.tables:
                    dim1val = self.eval(dim1)
                    dim2val = self.eval(dim2)
                    if dim1val < 1 or dim1val > len(self.tables[var]) or dim2val < 1 or dim2val > len(self.tables[var][0]):
                        print("TABLE INDEX OUT OUT BOUNDS AT LINE %s" %
                              self.stat[self.pc])
                        raise RuntimeError
                    return self.tables[var][dim1val - 1][dim2val - 1]
            print("UNDEFINED VARIABLE %s AT LINE %s" %
                  (var, self.stat[self.pc]))
            raise RuntimeError

    # Evaluate a relational expression
    def releval(self, expr):
        etype = expr[0]        
        if etype == 'GROUP':
            return self.releval(expr[1])
        elif etype == 'UNARY':
            if expr[1] == 'NOT':
                if (self.eval(expr[1]) == 0):
                    return 0
                else:
                    return 1 
            else:
                print 'BAD UNARY OPERATOR IN RELEXPR:',expr
                return 0
        elif etype == 'BINOP':
            ntype = expr[1]
            lhs = np.int32(self.eval(expr[2]))
            rhs = np.int32(self.eval(expr[3])) 
            if ntype == '<':
                if lhs < rhs:
                    return 1
                else:
                    return 0
            elif ntype == '<=':
                if lhs <= rhs:
                    return 1
                else:
                    return 0

            elif ntype == '>':
                if lhs > rhs:
                    return 1
                else:
                    return 0

            elif ntype == '>=':
                if lhs >= rhs:
                    return 1
                else:
                    return 0

            elif ntype == '=':
                if lhs == rhs:
                    return 1
                else:
                    return 0

            elif ntype == '<>':
                if lhs != rhs:
                    return 1
                else:
                    return 0
            elif ntype == 'AND':
                if lhs and rhs:
                    return 1
                else:
                    return 0
            elif ntype == 'OR':
                if lhs or rhs:
                    return 1
                else:
                    return 0
            elif ntype == '==':
                if lhs == rhs:
                    return 1
                else:
                    return 0                
            else:
                print "UNKNOWN OPERATOR IN RELEXPR", expr
                return 0 
        elif etype == 'RELOP':
            ntype = expr[1]
            lhs = np.int32(self.eval(expr[2]))
            rhs = np.int32(self.eval(expr[3])) 
            if ntype == '<':
                if lhs < rhs:
                    return 1
                else:
                    return 0
            elif ntype == '<=':
                if lhs <= rhs:
                    return 1
                else:
                    return 0

            elif ntype == '>':
                if lhs > rhs:
                    return 1
                else:
                    return 0

            elif ntype == '>=':
                if lhs >= rhs:
                    return 1
                else:
                    return 0

            elif ntype == '=':
                if lhs == rhs:
                    return 1
                else:
                    return 0

            elif ntype == '<>':
                if lhs != rhs:
                    return 1
                else:
                    return 0
            elif ntype == 'AND':
                if lhs and rhs:
                    return 1
                else:
                    return 0
            elif ntype == 'OR':
                if lhs or rhs:
                    return 1
                else:
                    return 0
            elif ntype == '==':
                if lhs == rhs:
                    return 1
                else:
                    return 0                
            else:
                print "UNKNOWN OPERATOR IN RELEXPR", expr
                return 0
        else:
            print "UNKNOWN TYPE OF RELATIVE OPERATOR:", expr
            
    # Assignment
    def assign(self, target, value):
        var, dim1, dim2 = target
        if not dim1 and not dim2:
            x = self.eval(value)
            if type(x) is int:
                self.vars[var] = np.int32(self.eval(value))
            else:
                self.vars[var] = self.eval(value)
        elif dim1 and not dim2:
            # List assignment
            dim1val = self.eval(dim1)
            if not var in self.lists:
                self.lists[var] = [0] * 10

            if dim1val > len(self.lists[var]):
                print ("DIMENSION TOO LARGE AT LINE %s" % self.stat[self.pc])
                raise RuntimeError
            self.lists[var][dim1val - 1] = self.eval(value)
        elif dim1 and dim2:
            dim1val = self.eval(dim1)
            dim2val = self.eval(dim2)
            if not var in self.tables:
                temp = [0] * 10
                v = []
                for i in range(10):
                    v.append(temp[:])
                self.tables[var] = v
            # Variable already exists
            if dim1val > len(self.tables[var]) or dim2val > len(self.tables[var][0]):
                print("DIMENSION TOO LARGE AT LINE %s" % self.stat[self.pc])
                raise RuntimeError
            self.tables[var][dim1val - 1][dim2val - 1] = np.uint32(self.eval(value))

    # Change the current line number
    def goto(self, linenum):
        if not linenum in self.prog:
            print("UNDEFINED LINE NUMBER %d AT LINE %d" %
                  (linenum, self.stat[self.pc]))
            raise RuntimeError
        self.pc = self.stat.index(linenum)


    def has_variable(self,allvars,name):
        for var in allvars:
            if (var.name == name):
                return True
        return False 

    def has_statement(self,allstatements, lineno):
        for state in allstatements:
            if (state.lineno == lineno):
                return True
        return False 

    def find_variable(self,allvars,name):
        for var in allvars:
            if (var.name == name):
                return var
        return None

    # given a statement index, return the line number 
    def find_statement_index(self, allstatements,lineno):
        for i in range(len(allstatements)):
            state = allstatements[i]
            if (state.lineno == lineno):
                return i

        return None

    # returns a list of all the veriables in the RHS of an expression
    # this are the variables read by the expression 
    def find_expr_variables(self, all_vars, expr):

        if expr == None:
            return None
        
        etype = expr[0]

        if etype == 'NUM':
            retval = None 
        elif etype == 'GROUP':
            retval = self.find_expr_variables(all_vars,expr[1])
        elif etype == 'UNARY':
            retval = self.find_expr_variables(all_vars,expr[2])
        elif ((etype == 'BINOP') or (etype == 'RELOP')):
            vars1 = self.find_expr_variables(all_vars,expr[2])
            vars2 = self.find_expr_variables(all_vars,expr[3])
            if ((vars1 == None ) and (vars2 == None )):
                retval = None
            elif (vars1 == None):
                retval = vars2
            elif (vars2 == None):
                retval = vars1
            elif ( (type(vars1) is str) and (type(vars2) is str)):
                v12 = [vars1,vars2]
                retval = list(set(v12)) # use set to remove duplicates 
            elif ( (type(vars1) is str) and (type(vars2) is list) ):
                vars2.append(vars1)
                retval = list(set(vars2))
            elif ((type(vars1) is list) and (type(vars2) is str)):
                vars1.append(vars2)
                retval = list(set(vars1))
            elif ((type(vars1) is list) and (type(vars2) is list)):
                retval = list(set(vars1 + vars2)) # use set to remove duplicates
            else:
                print "Error parsing RHS variables! %s %s %s %s " % (str(vars1),str(vars2),type(vars1),type(vars2))
                retval = None
                
        elif etype == 'VAR':
            var, dim1, dim2 = expr[1]
            retval = [ var ] 
        else:
            print ("Error parsing expression to get vars in RHS: %s" % expr)
            return None

        return retval
                
    # start with the root statement and create backward edges
    # except for RETURN statements 
    def create_backward_edges(self, statement):
        statement.visited = True
        for s in statement.successors:
            foundself = False 
            if (s != None):
                # make sure the current statement is not in the list of predecessors 
                for p in s.predecessors:
                    if (p != None):
                        if (p.name == s.name):
                               foundself = True
                               break

                if (foundself == False):
                    s.predecessors.append(statement)
                    if (s.visited == False):
                        self.create_backward_edges(s)

        for s in statement.successors_taken:
            foundself = False 
            if (s != None) :
                # make sure the current statement is not in the list of predecessors 
                for p in s.predecessors:
                    if (p != None):
                        if (p.name == s.name):
                               foundself = True
                               break

                if (foundself == False):
                    s.predecessors_taken.append(statement)
                    if (s.visited == False):
                        self.create_backward_edges(s)            

    # Gosubs/returns use an extra pair of bits to signal where the return statement 
    # should return control to.
    #
    # The control bit c_bit_######_gosub signals the entry to the gosub statement
    #
    # That gosub statement then sets the bit c_bit_######_gosub_return, which the return
    # node uses to 'look up' from set of possible entry gosubs which control bit to
    # set next
    # using the gosub_return bits, the return sets the c_bit_XXXXX_return_YYYYY,
    # where XXXXX is the return line number and YYYYY is the target control node
    # to return to.
    # 
    # to find the matching return to a gosub statement.
    
    # This method takes a gosub root and statement
    # advances forward through the CFG looking for the matching RETURN statements. 
    # for each return, we add a list of matching gosubs to that return statement
    def find_return_successor(self, root_gosub,statement,all_statements):

        if statement.visited == True:
            return
        statement.visited = True
        
        if statement.type == 'RETURN':
            gosub_index = root_gosub.index
            next_statement = all_statements[gosub_index+1]
            statement.successors.append(next_statement)
            statement.gosub_statements.append(root_gosub)
            root_gosub.return_statement = statement
        else:
            for s in statement.successors:
                self.find_return_successor(root_gosub,s,all_statements)
            for s in statement.successors_taken:
                self.find_return_successor(root_gosub,s,all_statements)
        return 

    
    def print_control_flow_graph(self,f1,all_nodes):
        print >> f1, "Control Flow Graph:" 

        for st in sorted(all_nodes):
            print >> f1, ("line: %s successors:" % (st.name)),
                
            for su in st.successors:
                print >> f1, "line", su.name,

            print >> f1, " taken: ",                
            for su in st.successors_taken:
                print >> f1, "line", su.name,

            print >> f1, " predecessors: ",
            for su in st.predecessors:
                print >> f1, "line", su.name,

            print >> f1, " taken: ",
            for su in st.predecessors_taken:
                print >> f1, "line", su.name,
                
            print >> f1, (" ")

    # plot a graph of the nodes
    # def  plot_graph(self,all_nodes):
        # G=pgv.AGraph(strict=False,directed=True)
        # G.node_attr['shape']='ellipse'
        # for n in all_nodes:
        #     G.add_node(n.name)
        # for n1 in all_nodes:
        #     for n2 in n1.successors:
        #         G.add_edge(n1.name,n2.name,color='black')
        #     for n1 in n1.successors_taken:
        #         G.add_edge(n1.name,n2.name,color='black')
        #     for n1 in n1.predecessors:
        #         G.add_edge(n1.name,n2.name,color='red')
        #     for n1 in n1.predecessors_taken:
        #         G.add_edge(n1.name,n2.name,color='green')                
        # G.layout()
        # G.draw("/tmp/test1.png")
        
    # These are the verilog sections:
    # (1) header, (2) variables/state, (3) initialization, (4) dataflow, (5) control flow, (6) I/O and the (7) trailer. 
    def print_verilog_header(self, fd,module_name):
        print >> fd, ("module %s();" % (module_name)) 
        print >> fd, " \t "
        
    def print_verilog_var_section(self, fd, all_vars,var_size,all_nodes):
        print >> fd, " // -------- Variable Section  ----------"
        print >> fd, " // --- User Variables ---- "        
        for v in sorted(all_vars):
            print >> fd, (" \t reg signed [%d:0] %s" % (var_size-1,v.name)),
            for d in range(len(v.dimensions)):
                print >> fd, ("[0:%d] " % (v.dimensions[d])), # do not subtract 1, because basic 
            print >> fd, ";"                                  # arrays are 1..N, not 0..N-1
            
        print >> fd, " // --- Control Bits ---- "
        print >> fd, (" \t reg clk ; ")
        print >> fd, (" \t reg [63:0] cycle_count ; ")        
        
        for s in all_nodes:
            if ((s.type == 'IF') or (s.type == 'FORTEST') or (s.type == 'NEXTTEST')):
                print >> fd, (" \t reg c_bit_%s_taken ; " % (s.name))
            elif (s.type == 'GOSUB'):
                print >> fd, (" \t reg c_bit_%s_return ; " % (s.name))
            elif (s.type == 'RETURN'):
                for i in range(len(s.gosub_nodes)):
                    gosub_name = s.gosub_nodes[i].name 
                    target_name = s.return_targets[i].name                   
                    print >> fd, (" \t reg c_bit_%s_gosub_%s ; " % (s.name,gosub_name))
                    print >> fd, (" \t reg c_bit_%s_%s ; " % (s.name,target_name))
                continue; # a return does not have a global control bit to set, there is one for each statement 
            
            print >> fd, (" \t reg c_bit_%s ; " % (s.name))

    def print_verilog_initial(self, fd, all_vars,all_statements):
        print >> fd, " // -------- Initialization Section  ----------"
        print >> fd, " initial begin "
        print >> fd, " \t clk =0 ; "
        print >> fd, " \t cycle_count =0 ; "        
        print >> fd, " \t c_bit_00000_start = 1 ; "

        if (len(self.data) > 0):
            print >> fd, " // --- Data Array ---- "
            print >> fd, " \t basic_data_pointer = 0 ;"
            for i in range(len(self.data)):
                print >> fd, (" \t basic_data_array[%d]=%d ;" % (i,self.data[i]))

        print >> fd, "end // initial "
        
    def print_verilog_data_section(self, fd, all_vars,all_nodes,debug_vars):
        print >> fd, " // -------- Data Flow Section  ----------"
        
        for v in sorted(all_vars):
            print >> fd, ("always @(posedge clk) begin // dataflow for variable %s " % (v.name))
            print >> fd, " \t ",
            for n in v.write_nodes:

                if v.name in debug_vars:
                    debug = True
                    debug_line = "\t \t $display(\"VERILOG_DEBUG: cycle_count: %d updating: " + v.name + " value: %d at: "
                else:
                    debug = False
                    debug_line = " "
                    
                if (n.type == 'ASSIGN'):
                    if debug:
                        debug_line = debug_line + (("c_bit_%s" % (n.name))) + " statement: " + n.verilog[0] + "\",cycle_count," + v.name + ") ; \n"
                    print >> fd, ("\t if (c_bit_%s == 1) begin \n \t \t %s \n "%  (n.name,n.verilog[0])) + debug_line + "\t end \n \t else "

            # we don't add a self assignment to avoid latches if the variable is an array
            if (len(v.dimensions) == 0):
                print >> fd, ("\t begin \n \t \t %s <= %s ; \n \t end" % (v.name,v.name))
            else:
                print >> fd, ("\t begin \n \t \t \n \t end" )                
            print >> fd, " "
            print >> fd, "end \n "

    def print_verilog_IO_section(self,fd,all_vars,all_nodes):
        print >> fd, " // -------- I/O Section  ----------"
        print >> fd, "always @(posedge clk) begin "
        print >> fd, " \t ",
        for n in all_nodes:
            if (n.type == "PRINT"):
                print >> fd, ("if (c_bit_%s == 1) begin \n \t \t %s \n \t end \n \t " % (n.name,n.verilog[0]))
        print >> fd, "end \n "
        
    def print_verilog_control_section(self,fd,all_vars,all_nodes,debug_range):
        print >> fd, " // -------- Control Flow Section  ----------"
        # debug range are the line numbers for which we want to add debugging $display statements
        if (len(debug_range) >=2 ):
            debug_low = debug_range[0]
            debug_high = debug_range[1]
        else:
            debug_low = 0
            debug_high = 0

        for node in all_nodes[1:]:
            all_my_preds = []
            for n in node.predecessors:
                # for a RETURN, each possible successor gets a control node by the name of the node 
                if (n.type == 'RETURN'):
                    all_my_preds.append("c_bit_" + n.name + "_" + node.name)                    
                else:
                    all_my_preds.append("c_bit_" + n.name)

            for n in node.predecessors_taken:
                all_my_preds.append("c_bit_" + n.name + "_taken")
                
            print >> fd, ("always @(posedge clk) begin // control for line %s " % node.name)
            name = node.name
            lineno = node.lineno
            entry_verilog = " "

            for i in range(len(all_my_preds)-1):
                    c = all_my_preds[i]
                    entry_verilog = entry_verilog + "(" + c + " == 1) || "

            if ( len(all_my_preds) >0 ):  # a statement could have not predecessors, dead code
                c = all_my_preds[len(all_my_preds)-1]
                entry_verilog = entry_verilog + "(" + c + " == 1) "
            else:
                entry_verilog = entry_verilog + "(" + "0" + " == 1) "
                
            print >> fd, " \t if (" + entry_verilog + ") begin "                
            if ( (lineno >= debug_low ) and (lineno <= debug_high)):
                print >> fd, "\t $display (\"VERILOG_DEBUG: cycle_count: %d at : %s\",cycle_count," + "\""+ name + "\" ); "

            # the first statement has to set the START bit back to zero 
            if ( node.index == 0):
                print >> fd, "\t c_bit_00000_start <= 0; ",
                
            if (node.type == 'IF'):
                print >> fd, (" \t \t " + node.verilog[0] + " \n \t  \t \t \t c_bit_%s_taken <= 1 ; c_bit_%s <=0 ; \n \t \t \t end // if taken\n \t \t else begin \n \t \t \t \t c_bit_%s <= 1; c_bit_%s_taken <= 0; end \n \t end " % (name,name,name,name)) 
                print >> fd, (" \t else begin \n \t \t c_bit_%s <= 0; c_bit_%s_taken <=0 ; end " % (name,name))

            elif (node.type == 'FORTEST'):
                print >> fd, ("\t \t "+ node.verilog[0]) 
                print >> fd, ("\t \t \t " + node.verilog[1])
                print >> fd, (" \t \t \t \t c_bit_%s_taken <= 1 ; c_bit_%s <=0 ; \n \t \t \t end // loop exit, taken\n \t \t \t else begin \n \t \t \t \t c_bit_%s_taken <= 0; c_bit_%s <= 1; \n \t \t \t end " % (name,name,name,name))
                print >> fd, ("\t \t end else begin")
                print >> fd, ("\t \t \t " + node.verilog[2])
                print >> fd, (" \t \t \t \t c_bit_%s_taken <= 1 ; c_bit_%s <= 0 ; \n \t \t \t \t end // loop exit, taken\n \t \t \t else begin \n \t \t \t \t c_bit_%s_taken <= 0; c_bit_%s <= 1; \n \t \t \t end \n \t \t end  " % (name,name,name,name))
                print >> fd, (" \t end ")
                print >> fd, (" \t else begin \n \t \t c_bit_%s <= 0; c_bit_%s_taken <=0 ; \n \t end " % (name,name))
                
            elif (node.type == 'NEXTTEST'):
                print >> fd, ("\t \t "+ node.verilog[0]) 
                print >> fd, ("\t \t \t " + node.verilog[1])
                print >> fd, (" \t \t \t \t c_bit_%s_taken <= 1 ; c_bit_%s <=0 ; \n \t \t \t end // loop exit, taken\n \t \t \t else begin \n \t \t \t \t c_bit_%s_taken <= 0; c_bit_%s <= 1; \n \t \t \t end " % (name,name,name,name))
                print >> fd, ("\t \t end else begin")
                print >> fd, ("\t \t \t " + node.verilog[2])
                print >> fd, (" \t \t \t \t c_bit_%s_taken <= 1 ; c_bit_%s <= 0 ; \n \t \t \t \t end // loop exit, taken\n \t \t \t else begin \n \t \t \t \t c_bit_%s_taken <= 0; c_bit_%s <= 1; \n \t \t \t end \n \t \t end  " % (name,name,name,name))
                print >> fd, (" \t end ")
                print >> fd, (" \t else begin \n \t \t c_bit_%s <= 0; c_bit_%s_taken <=0 ; \n \t end " % (name,name))

            elif (node.type == 'GOSUB'):
                ret_name = node.statement.return_statement.control_nodes[0].name
                print >> fd, (" \t \t c_bit_%s  <= 1; " % name)
                print >> fd, (" \t \t c_bit_%s_return <= 1; \n \t end " % name)
                print >> fd, (" \t else if (c_bit_%s_gosub_%s == 1) begin " % (ret_name,node.name))
                if ( (lineno >= debug_low ) and (lineno <= debug_high)):
                    print >> fd, "\t \t $display (\"VERILOG_DEBUG: cycle_count: %d at : %s_return\",cycle_count," + "\""+ name + "\" ); "
                print >> fd, ("\t \t c_bit_%s_return <= 0 ; \n \t \t c_bit_%s <= 0; \n \t \t end " % (name,node.name))
                    
                print >> fd, ("\t else begin \n \t \t c_bit_%s <=0 ; \n \t \t c_bit_%s_return <= c_bit_%s_return ; \n \t end " % (node.name,node.name,node.name))
                
            elif (node.type == 'RETURN'):
                for i in range(len(node.gosub_nodes)):
                    gosub_name = node.gosub_nodes[i].name 
                    target_name = node.return_targets[i].name                   
                    print >> fd, ("\t \t if (c_bit_%s_return == 1) begin \n \t \t \t c_bit_%s_gosub_%s <= 1 ; " % (gosub_name, name,gosub_name))
                    print >> fd, ("\t \t \t c_bit_%s_%s <= 1; \n \t \t end \n " % (name,target_name))
                    if (i < len(node.gosub_nodes)-1):
                        print >> fd, " \t \t else ",

                print >> fd, "\t end \n \t else begin"
                for i in range(len(node.gosub_nodes)):
                    gosub_name = node.gosub_nodes[i].name 
                    target_name = node.return_targets[i].name
                    # The names of the gosub bit and targets must be 
                    # distinct, so there is an extra gosub inbetween for the
                    # control bit for the gosub return, as opposed to the target 
                    print >> fd, ("\t \t c_bit_%s_gosub_%s <= 0 ; " % (name,gosub_name))
                    print >> fd, ("\t \t c_bit_%s_%s <= 0 ; " % (name,target_name))
                print >> fd, "\t end"
                
            elif (node.type == "END"):
                 print >> fd, (" \t \t c_bit_%s <= 1 ; $finish; \n \t end \n \t else " % (name)),
                 print >> fd, ("begin \n \t \t c_bit_%s <= 0 ; \n \t end" % (name))
            else:
                print >> fd, (" \t \t c_bit_%s <= 1 ;  \n \t end \n \t else " % (name)),
                print >> fd, ("begin \n \t \t c_bit_%s <= 0 ; \n \t end" % (name))

            print >> fd, "end // end @ posedge clk "
            print >> fd, " "
            
    def print_verilog_trailer(self,fd, module_name):
        print >> fd, " // -------- Trailer Section  ----------"
        print >>fd, " \t // cycle counter"        
        print >> fd, "always @(posedge clk) begin"
        print >> fd, " \t if (cycle_count > 50000) begin ",
        print >> fd, " \t \t $display(\"reached maximum cycle count of 50000\");" 
        print >> fd, " \t \t  $finish;" 
        print >> fd, " \t end" 
        print >> fd, " \t else begin" 
        print >> fd, " \t \t cycle_count <= cycle_count + 1 ;"
        print >> fd, "\t end"
        print >> fd, " end "
        print >> fd, " "
        print >>fd, " \t // clock generator"        
        print >>fd, " \t always"
        print >>fd, " \t \t #1 clk = !clk ; "
        print >>fd, ("endmodule // %s" % (module_name))
        print >> fd, " "        
        
    # output a verilog version of this program 
    def output_verilog(self):
        # get the list of variables
        verilog_variables = {}
        verilog_arrays = {}
        verilog_inital = {}

        all_statements = []   # list of all statements an a control flow graph of them
        all_variables = []    # list of all variables. 
        all_controlnodes = []  # list of all the control nodes for a control flow graph of them 
        all_gosub_statements = [] # lists all gosub statements 
        global inside_relational_expression            

        # first pass : get all statements and variables
        # Variables can be defined in DIM statements, LET statements and FOR statements

        # for data-statements we need a pointer and an array
        if (len(self.data) > 0):
            basic_data_pointer = Variable("basic_data_pointer", [])
            all_variables.append(basic_data_pointer)         
            basic_data_array = Variable("basic_data_array", [len(self.data)])
            all_variables.append(basic_data_array)
        
            pointer_var = self.find_variable(all_variables,"basic_data_pointer")
            data_var = self.find_variable(all_variables,"basic_data_array")
                
        self.inside_verilog_str = True
        for pc in range(len(self.stat)):
            lineno = self.stat[pc]            
            instr = self.prog[lineno]
            op = self.prog[lineno][0]

            statement = StatementNode(pc,lineno,op,instr)
            all_statements.append(statement)
            global inside_relational_expression # hack to print == vs = when creating verilog statements 
            inside_relational_expression = False 
            
            if (op == 'DIM'):
                for vname, x, y in instr[1]:
                    if (self.has_variable(all_variables,vname) == True):
                        continue
                    if y == 0:
                        # Single dimension variable
                        newvar = Variable(vname, [x])
                    else:
                        newvar = Variable(vname,[x,y])

                    all_variables.append(newvar) 

            elif ((op == 'LET') or (op == 'FIFO')):
                vname = instr[1][0]
                if (self.has_variable(all_variables,vname) == False):
                    if (op == 'FIFO'):
                        newvar = Variable(('(f_'+vname), [])
                        newvar.isfifo = True
                    else:
                        newvar = Variable(vname, [])
                    all_variables.append(newvar)

            elif (op == 'READ'):
                vname = instr[1][0][0]
                if (self.has_variable(all_variables,vname) == False):
                    newvar = Variable(vname, [])
                    all_variables.append(newvar)

            elif op == 'FOR':
                loopvar = instr[1]
                if (self.has_variable(all_variables,loopvar) == False):
                    newvar = Variable(loopvar, [])
                    all_variables.append(newvar)                
            else:
                pass

        # second pass: 
        # build a forward Statement-level Control FLow Graph 
        # also builds predecessor (backward) edges, except for
        # RETURN statements which require another pass

        for pc in range(len(self.stat)):
            lineno = self.stat[pc]   # line number in the program 
            instr = self.prog[lineno]
            op = self.prog[lineno][0]

            statement = all_statements[pc]
            
            # the default sucessor statement is the next statement in lexical order 
            if (pc < (len(self.stat)-1)):
                nextlineno = (self.stat[pc+1])
                nextstatement = all_statements[pc+1]
            else:
                nextlineno = 0
                nextstatement = None

            # the defaul predicessor statement is the prior statement in lexical order
            # because we do not have a START statement (i.e. the inverse of the END) we
            # create a fake START statment with line number 0
            
            if (pc == 0):
                prevlineno = -1
                nexts = all_statements[0]
                startstatement = StatementNode(-1,-1,'START',['START'])
                startstatement.lineno = 0
                startstatement.name = str(0)
                startstatement.successors.append(nexts)                
                prevstatement = startstatement
            else:
                prevlineno = (self.stat[pc-1])
                prevstatement = all_statements[pc-1]
                
            # LET maps to assignment
            if op == 'LET':
                target = instr[1][0]
                target_str = self.verilog_var_str(instr[1])
                type = instr[2][0]
                value = "0"

                # 1. statement variable section
                rhs_vars = self.find_expr_variables(all_variables,instr[2])
                #print "LET RHS: " + str(rhs_vars)

                if type == 'NUM':
                    # hack to create string type from nums 
                    value = str(instr[2][1])
                    if (not (value.isdigit())):
                        value = "\"" + value + "\""
                        
                elif type == 'VAR':
                    value = self.verilog_var_str(instr[2][1])
                elif ((type == 'BINOP') or (type == 'UNARY') or (type == 'GROUP')):
                    value = self.expr_str(instr[2])                    
                elif (type == None):
                    value = None

                if (value != None):
                    var = self.find_variable(all_variables,target)
                    if (var != None):
                        statement.write_vars.append(var)
                    else:
                        print ("Statement %s variable %s not found!!" % (instr, value))

                statement.write_vars.append(var) 
                statement.read_vars = rhs_vars
                var.write_statements.append(statement)
                
                # 3. statement verilog section
                statement.verilog.append(target_str + " <= " + value + " ;" )
                
                # 2. statement control flow graph section
                statement.successors.append(nextstatement)
                                
                # 4. Control Node section
                assign_name = ('%05d_00_assign' % (statement.lineno ))
                assign_node = ControlNode('ASSIGN',statement,len(all_controlnodes),assign_name,lineno)
                assign_node.write_vars.append(var)
                assign_node.read_vars.append(rhs_vars)
                assign_node.verilog.append(statement.verilog[0])
                all_controlnodes.append(assign_node)
                statement.control_nodes.append(assign_node)
                var.write_nodes.append(assign_node)

                bubble_name = ('%05d_01_bubble' % (statement.lineno ))
                bubble_node = ControlNode('BUBBLE',statement,len(all_controlnodes),bubble_name,lineno)
                all_controlnodes.append(bubble_node)
                statement.control_nodes.append(bubble_node)

                # 5. intra-statement CFG edges 
                assign_node.successors.append(bubble_node)

            elif op == 'FIFO':

                statement.successors.append(nextstatement)
                
                bubble_name = ('%05d_00_bubble' % (statement.lineno ))
                bubble_node = ControlNode('BUBBLE',statement,len(all_controlnodes),bubble_name,lineno)
                all_controlnodes.append(bubble_node)
                statement.control_nodes.append(bubble_node)
                
            elif op == 'READ':

                if (len(self.data) == 0):
                    print ("ERROR. READ WITH NO DATA AT LINE %d" % (statement.lineno))
                    self.error=1
                    return 
                    
                rhs_vars = []
                rhs_vars_str = []

                for target in instr[1]:
                    rhs_vars.append(instr[1][0])
                    rhs_vars_str.append(self.verilog_var_str(target))

                statement.successors.append(nextstatement)

                # for each node in the RHS variables, add an assignment statement and bubble
                for i in range(len(rhs_vars)):
                    target_var = self.find_variable(all_variables,rhs_vars[i][0])
                    if (target_var == None):
                        print ("error, no var %s found for read statement" % (str(rhs_vars[i][0])))
                    target_str = rhs_vars_str[i]

                    # First assign the variable from the data array 
                    assign_name = ('%05d_%02d_assign' % (statement.lineno,i))
                    assign_node = ControlNode('ASSIGN',statement,len(all_controlnodes),assign_name,lineno)
                    all_controlnodes.append(assign_node)
                    statement.control_nodes.append(assign_node)
                    assign_node.verilog.append(target_str + " <= basic_data_array[basic_data_pointer] ;" )
                    target_var.write_nodes.append(assign_node)
                    data_var.read_nodes.append(assign_node)
                    pointer_var.read_nodes.append(assign_node)
                    
                    update_name = ('%05d_%02d_update' % (statement.lineno,i))
                    update_node = ControlNode('ASSIGN',statement,len(all_controlnodes),update_name,lineno)
                    all_controlnodes.append(update_node)
                    statement.control_nodes.append(update_node)
                    update_node.verilog.append("basic_data_pointer <= basic_data_pointer + 1;" )
                    pointer_var.write_nodes.append(update_node)
                    pointer_var.read_nodes.append(update_node)
                    
                    bubblename = ('%05d_%02d_bubble' % (statement.lineno,i))
                    bubblenode = ControlNode('BUBBLE',statement,len(all_controlnodes),bubblename,lineno)
                    all_controlnodes.append(bubblenode)
                    statement.control_nodes.append(bubblenode)

                # update the inter-statement list of control nodes 
                for i in range(len(statement.control_nodes)-1):
                    statement.control_nodes[i].successors.append(statement.control_nodes[i+1])
            elif op == 'DIM':
                for vname, x, y in instr[1]:
                    if y == 0:
                        # Single dimension variable
                        verilog_variables[vname] = str(x)
                    else:
                        # Double dimension variable
                        verilog_variables[vname] = [str(x),str(y)]

                statement.successors.append(nextstatement)

                # put a placeholder control node for now 
                control_name = ('%05d_dim' % (statement.lineno ))
                control_node = ControlNode('DIM',statement,len(all_controlnodes),control_name,lineno)
                all_controlnodes.append(control_node)
                statement.control_nodes.append(control_node)
                
            elif op == 'FUNC':
                statement.successors.append(nextstatement)

                # put a placeholder control node for now 
                control_name = ('%05d_func' % (statement.lineno ))
                control_node = ControlNode('FUNC',statement,len(all_controlnodes),control_name,lineno)
                all_controlnodes.append(control_node)
                statement.control_nodes.append(control_node)
                
            # print maps to a $display statement with a format and arguments                     
            elif op == 'PRINT': 
                plist = instr[1]
                format = ""
                args = ""
                for label, val in plist:
                    type = val[0]
                    if (label): 
                        format = format + "%s"
                        args = args + ",\"" + label + "\""
                    elif type == 'VAR':
                        if (str(val[1][0]) == 'TOHEX'): 
                            format = format + "%0x"
                        else: 
                            format = format + "%0d"
                        args = args + "," + self.expr_str(val)
                    elif type == 'NUM':
                        format = format + "%0s"
                        args = args + ',\"' + self.expr_str(val) + '\"'
                        
                statement.successors.append(nextstatement)
                statement.verilog.append("\t \t $display(\"" + format + "\""+args+ ");")

                print_name = ("%05d_print" % (statement.lineno ))
                control_node = ControlNode('PRINT',statement,len(all_controlnodes),print_name,statement.lineno)
                control_node.verilog.append(statement.verilog[0]) 
                all_controlnodes.append(control_node)
                statement.control_nodes.append(control_node)                
                
            elif op == 'FOR':
                loopvar = instr[1]
                initval = instr[2]
                finval = instr[3]
                stepval = instr[4]

                continuestatement = all_statements[pc+1]  # loop body statement 
                n = self.loopend[pc]                      # this it the corresponding next statement
                exitstatement = all_statements[n+1]       #the statement after the next is the target 

                # 1. statement variable section
                var = self.find_variable(all_variables,loopvar)
                if (var != None):
                    statement.write_vars.append(var)
                else:
                    print ("Statement %s variable %s not found!!" % (str(instr), str(loopvar)))

                rhs_vars = [ loopvar ] 
                initvars = self.find_expr_variables(all_variables,initval)
                finvars =  self.find_expr_variables(all_variables,finval)
                stepvars = self.find_expr_variables(all_variables,stepval)
                                
                if (initvars != None):
                    rhs_vars = rhs_vars + initvars
                    
                statement.read_vars = rhs_vars
                statement.write_vars.append(var)

                # 2. statement control flow graph section
                statement.successors.append(nextstatement)
                statement.successors_taken.append(exitstatement)
                
                # 3. statement verilog section
                if (stepval == None ):
                    increment_string = "1"
                else:
                    increment_string = self.expr_str(stepval)
                    
                statement.verilog.append ("if ( (" + str(loopvar) + ") > " + self.expr_str(finval) + ") begin " )
                #the first element of verilog tests if the loop is increasing or decreasing 
                statement.verilog.append ("if ( (" + increment_string + ") > 0 ) begin " )
                                          
                #the second element of verilog tests exit in the positive direction 
                statement.verilog.append ("if ( (" + str(loopvar) + ") > " + self.expr_str(finval) + ") begin " )
                                          
                #the third element of verilog tests exit in the negative direction
                statement.verilog.append ("if ( (" + str(loopvar) + ") < " + self.expr_str(finval) + ") begin " )
                statement.verilog.append("\t \t " + loopvar + " <= " + self.expr_str(initval) + " ;")
                
                # 4. Control Node section
                
                # first  control node is the loop test with the target exit
                # this is the test statement for the top of the loop
                # we add another statementnode in the graph which acts like an
                # IF but with a more complicated condition
                
                assign_index = len(all_controlnodes)
                assign_name  = ("%05d_%02d_assign" % (statement.lineno,0))
                assign_node = ControlNode('ASSIGN',statement,assign_index,assign_name,statement.lineno)
                all_controlnodes.append(assign_node)
                statement.control_nodes.append(assign_node)
                assign_node.write_vars.append(var)
                assign_verilog =  ("\t \t " + loopvar + " <= " + self.expr_str(initval) + " ;")
                assign_node.verilog.append(assign_verilog)                
                var.write_nodes.append(assign_node)
                

                # add a bubble to the FOR statement assignment
                bubble_index = len(all_controlnodes)
                bubble_name  = ("%05d_%02d_bubble" % (statement.lineno,1))
                bubble_node = ControlNode('BUBBLE',statement,bubble_index,bubble_name,statement.lineno)
                all_controlnodes.append(bubble_node)
                statement.control_nodes.append(bubble_node)

                test_index = len(all_controlnodes)
                test_name  = ("%05d_%02d_test" % (statement.lineno,2))
                test_node = ControlNode('FORTEST',statement,test_index,test_name,statement.lineno)
                all_controlnodes.append(test_node)
                statement.control_nodes.append(test_node)

                #the first element of verilog tests if the loop is increasing or decreasing 
                test_node.verilog.append ("if ( (" + increment_string + ") > 0 ) begin " )
                #the second element of verilog tests exit in the positive direction 
                test_node.verilog.append ("if ( (" + str(loopvar) + ") > " + self.expr_str(finval) + ") begin " )
                #the third element of verilog tests exit in the negative direction
                test_node.verilog.append ("if ( (" + str(loopvar) + ") < " + self.expr_str(finval) + ") begin " )
                
                # 5. intra-statement CFG edges 
                assign_node.successors.append(bubble_node)
                bubble_node.successors.append(test_node)
                
            # set the PC to the line after the for loop
            elif op == 'NEXT':
                n = self.looptarget[pc]
                # these are from the FOR statement 
                source_lineno = self.stat[n]
                source_instr = self.prog[source_lineno]
                source_loopvar = source_instr[1]
                source_initval = source_instr[2]
                source_finval  = source_instr[3]
                source_stepval = source_instr[4]

                # statement after the for statement
                continuestatement = all_statements[n+1]
                # statement before the NEXT statement
                prevstatement = all_statements[pc-1]    

                # 1. statement variable section 
                var = self.find_variable(all_variables,source_loopvar)
                if (var != None):
                    statement.write_vars.append(var)
                else:
                    print ('Statement %s variable %s not found!!' % (str(source_instr), str(source_loopvar)))
                var.write_statements.append(statement)                

                if (source_stepval == None ):
                    increment_string = "1"
                else:
                    increment_string = self.expr_str(source_stepval) 

                rhs_vars = [ loopvar ] 
                finvars =  self.find_expr_variables(all_variables,source_finval)
                if (finvars != None): 
                    rhs_vars = rhs_vars + self.find_expr_variables(all_variables,source_finval)
                statement.read_vars = rhs_vars

                # 2. statement control flow graph section
                # note that for a NEXT statement, taken means the condition is true,
                # which means we exit the loop. continue in this case means the condition
                # is false, which means we got back up the loop again 
                statement.successors.append(continuestatement)
                statement.successors_taken.append(nextstatement)
                
                # statement verilog section
                if (source_stepval == None ):
                    increment_string = "1"
                else:
                    increment_string = self.expr_str(source_stepval)
                    
                #the first element of verilog tests if the loop is increasing or decreasing 
                statement.verilog.append ("if ( (" + increment_string + ") > 0 ) begin " )
                                          
                #the second element of verilog tests exit in the positive direction 
                statement.verilog.append ("if ( (" + str(source_loopvar) + " + " + increment_string + ") > " + self.expr_str(source_finval) + ") begin " )
                                          
                #the third element of verilog tests exit in the negative direction
                statement.verilog.append ("if ( (" + str(source_loopvar) + " + " + increment_string + ") < " + self.expr_str(source_finval) + ") begin " )
                    
                #the verilog element is for the increment
                statement.verilog.append(" " + str(source_loopvar) + " <= " + str(source_loopvar) + " + " + increment_string + " ;")

                                
                # 3. Control Node section 

                # this is the test statement for the bottom of the FOR/NEXT loop
                # we need this because basic loops are inclusive
                # that is, for i = 10 to 10 would get executed once 
                # we add another statementnode in the graph which acts like an
                # IF but with a more complicated condition
                # note the bottom of the loop has a different condition than the top
                # as we need to add the 
                
                test_index = len(all_controlnodes)
                test_name  = ("%05d_%02d_test" % (statement.lineno,0))
                test_node = ControlNode('NEXTTEST',statement,test_index,test_name,statement.lineno)
                all_controlnodes.append(test_node)
                statement.control_nodes.append(test_node)
                test_node.read_vars = statement.read_vars
                

                #the first element of verilog tests if the loop is increasing or decreasing 
                test_node.verilog.append ("if ( (" + increment_string + ") > 0 ) begin " )
                #the second element of verilog tests exit in the positive direction 
                test_node.verilog.append ("if ( (" + str(source_loopvar) + " + " + increment_string + ") > " + self.expr_str(source_finval) + ") begin " )
                #the third element of verilog tests exit in the negative direction
                test_node.verilog.append ("if ( (" + str(source_loopvar) + " + " + increment_string + ") < " + self.expr_str(source_finval) + ") begin " )

                # this is the assignment control node if the test falls through 
                assign_index = len(all_controlnodes)
                assign_name  = ("%05d_%02d_assign" % (statement.lineno,1))
                assign_node = ControlNode('ASSIGN',statement,assign_index,assign_name,statement.lineno)
                all_controlnodes.append(assign_node)
                statement.control_nodes.append(assign_node)
                assign_node.write_vars.append(var)
                var.write_nodes.append(assign_node)
                assign_verilog =  (" " + str(source_loopvar) + " <= " + str(source_loopvar) + " + " + increment_string + " ;")
                assign_node.verilog.append(assign_verilog)
                
                # add a bubble to the NEXT statement assignment
                bubble_index = len(all_controlnodes)
                bubble_name  = ("%05d_%02d_bubble" % (statement.lineno,2))
                bubble_node = ControlNode('BUBBLE',statement,bubble_index,bubble_name,statement.lineno)
                all_controlnodes.append(bubble_node)
                statement.control_nodes.append(bubble_node)

                # intra-statement CFG edges 
                test_node.successors.append(assign_node)
                assign_node.successors.append(bubble_node)

            elif op == 'IF':
                relop = instr[1]
                targetlineno = instr[2]
                t = self.find_statement_index(all_statements,targetlineno)
                targetstatement = all_statements[t]

                if (targetstatement == None):
                    print('Error! no statement for line %d' % (targetlineno))

                # 1. statement variable section
                rhs_vars = self.find_expr_variables(all_variables,relop)
                statement.read_vars = rhs_vars 

                # 2. statement control flow graph section
                statement.successors.append(nextstatement)
                statement.successors_taken.append(targetstatement)

                # 3. statement verilog section
                inside_relational_expression = True
                statement.verilog.append("if (" + self.relexpr_str(relop) + ") begin ")
                inside_relational_expression = False

                # 4. Control Node section 
                test_index = len(all_controlnodes)
                test_name  = ("%05d_test" %(statement.lineno))
                test_node = ControlNode('IF',statement,test_index,test_name,statement.lineno)
                all_controlnodes.append(test_node)
                statement.control_nodes.append(test_node)
                inside_relational_expression = True                
                test_node.verilog.append("if (" + self.relexpr_str(relop) + ") begin ")
                inside_relational_expression = False
                
            elif op == 'GOTO':
                targetlineno = instr[1]
                t = self.find_statement_index(all_statements,targetlineno)
                targetstatement = all_statements[t]

                # 1. statement vars section

                # 2. statement control flow graph section
                statement.successors.append(targetstatement)

                # 3. statement Control Node section 
                bubble_index = len(all_controlnodes)
                bubble_name  = ("%05d_bubble" % (statement.lineno))
                bubble_node = ControlNode('BUBBLE',statement,bubble_index,bubble_name,statement.lineno)
                all_controlnodes.append(bubble_node)
                statement.control_nodes.append(bubble_node)
                
                
            elif op == 'GOSUB':
                targetlineno = instr[1]
                t = self.find_statement_index(all_statements,targetlineno)
                if (t == None):
                    print "Missing gosub target line at line:", lineno
                    sys.exit(-1)
                targetstatement = all_statements[t]
                all_gosub_statements.append(statement) 
                statement.successors.append(targetstatement)
                targetstatement.gosub_statements.append(statement)

                gosub_index = len(all_controlnodes)
                gosub_name  = ("%05d_gosub" % (statement.lineno))
                gosub_node = ControlNode('GOSUB',statement,gosub_index,gosub_name,statement.lineno)
                all_controlnodes.append(gosub_node)
                statement.control_nodes.append(gosub_node)

            elif op == 'REM':
                statement.successors.append(nextstatement)

                bubble_index = len(all_controlnodes)
                bubble_name  = ("%05d_bubble" % statement.lineno)
                bubble_node = ControlNode('BUBBLE',statement,bubble_index,bubble_name,statement.lineno)
                all_controlnodes.append(bubble_node)
                statement.control_nodes.append(bubble_node)

            elif op == 'RETURN':
                # the next statement in listing order is not the successor statement, the statement 
                # in listing order after the corresponding gosub is 
                return_index = len(all_controlnodes)
                return_name  = ("%05d_return" % statement.lineno)
                return_node = ControlNode('RETURN',statement,return_index,return_name,statement.lineno)
                all_controlnodes.append(return_node)
                statement.control_nodes.append(return_node)
                
            elif op == 'DATA':
                statement.successors.append(nextstatement)

                bubble_index = len(all_controlnodes)
                bubble_name  = ("%05d_bubble" % (statement.lineno))
                bubble_node = ControlNode('BUBBLE',statement,bubble_index,bubble_name,statement.lineno)
                all_controlnodes.append(bubble_node)
                statement.control_nodes.append(bubble_node)

            elif op == 'END':
                # cause and infinite loop at the end 
                statement.successors.append(statement)                

                end_index = len(all_controlnodes)
                end_name  = ( "%05d_end" % (statement.lineno))
                end_node = ControlNode('END',statement,end_index,end_name,statement.lineno)
                all_controlnodes.append(end_node)
                statement.control_nodes.append(end_node)

        # Crawl the CFG in the forward direction until we find a return
        # Mark the possible sucessors of the RETURN as the GOSUB statement
        # Each gosub/return pair as a bit set by the gosub and used by the return.
        # The return node sets one of N possible return bits, depending on the gosub
        # each successor to a return uses its matching return bit.

        for g in all_gosub_statements: 
            for s in all_statements:
                s.visited = False
            self.find_return_successor(g,g,all_statements)


        # create the forward edges for the control node graph
        # this section creates the edges between control nodes which are 
        # inter-statement, i.e. control nodes edges between statements, not within a statement
        for s in all_statements:
            s.visited = False
            # pythonic way to get the last element 
            last_control_node = s.control_nodes[-1]

            # if there is only one control node, the node's successor is always whatever the
            # statement's successor is
            if (s.type == 'END'):
                s.control_nodes[0].successors.append(s.control_nodes[0])
            elif (s.type == 'LET'):
                s.control_nodes[1].successors.append(s.successors[0].control_nodes[0])
            elif (s.type == 'IF'):
                s.control_nodes[0].successors.append(s.successors[0].control_nodes[0])
                s.control_nodes[0].successors_taken.append(s.successors_taken[0].control_nodes[0])
            elif (s.type == 'FOR'):
                # the test node has index 2
                s.control_nodes[2].successors.append(s.successors[0].control_nodes[0])
                s.control_nodes[2].successors_taken.append(s.successors_taken[0].control_nodes[0])
            elif (s.type == 'NEXT'):
                s.control_nodes[0].successors_taken.append(s.successors_taken[0].control_nodes[0])
                s.control_nodes[2].successors.append(s.successors[0].control_nodes[0])
            elif (s.type == 'RETURN'):
                for succ in s.successors:
                    last_control_node.successors.append(succ.control_nodes[0])
            elif (s.type == 'READ'):
                last_node = s.control_nodes[-1]
                last_node.successors.append(s.successors[0].control_nodes[0])
            elif (len(s.control_nodes) == 1):
                if (len(s.successors) ==1) :
                    last_control_node.successors.append(s.successors[0].control_nodes[0])
                else:
                    print "Error,statement control node does not have sucessors :" + s.name + " " + last_control_node.name 
            else:
                print "Error,statement types does not match known control node sequence"

        # this pass through the nodes set the gosub returns for the control flow graph
        for s in all_statements:
            if (s.type == 'RETURN'):
                # get the control node for the return statement, and append the list of control
                # nodes from the statement's list of gosub nodes
                # the return target is the successor node to the gosub node 
                return_node = s.control_nodes[0]
                for g in s.gosub_statements: 
                    return_node.gosub_nodes.append(g.control_nodes[0])
                    next_statement = all_statements[g.index+1] 
                    return_node.return_targets.append(next_statement.control_nodes[0])
        

        # add the start control node to the front of the list off all control nodes 
        start_index = 0
        start_name  = ("%05d_start" % (0))
        start_node = ControlNode('START',statement,start_index,start_name,-1)
        start_node.successors.append(all_controlnodes[0])
        all_controlnodes.insert(0,start_node)

        # create backward edges for the whole statement graph 
        for s in all_statements:
            s.visited = False 
        self.create_backward_edges(startstatement)


        #print >> f1, "Control node CFG forward edges"
        #self.print_control_flow_graph(f1,all_controlnodes)
        
        # create backward edges in the control node graph 
        for n in all_controlnodes:
            n.visted = False
        self.create_backward_edges(all_controlnodes[0])

        #f1 = sys.stdout
        #print >> f1, "Statement Node graph before gosub"
        #self.print_control_flow_graph(f1,all_statements)

        #print >> f1, "Control Node full graph"
        #self.print_control_flow_graph(f1,all_controlnodes)

        #self.plot_graph(all_controlnodes)

        # this is the output file name. Default is a.out
        f1=open(self.program_args['output'], 'w')

        # these need to made into options 
        module_name = "basic"
        # to change size of a integer change this variable 
        variable_size = 32
        debug_range = [0,0]
        debug_vars = [ ]

        # sort all the statement nodes in line-number order 
        all_statements.sort()
        all_controlnodes.sort()
        
        # output the verilog 
        self.print_verilog_header(f1,module_name)
        self.print_verilog_var_section(f1,all_variables,variable_size,all_controlnodes)
        self.print_verilog_initial(f1, all_variables,all_controlnodes)
        self.print_verilog_data_section(f1,all_variables,all_controlnodes,debug_vars)
        self.print_verilog_IO_section(f1,all_variables,all_controlnodes)
        self.print_verilog_control_section(f1,all_variables,all_controlnodes,debug_range)
        self.print_verilog_trailer(f1,module_name)

        # control if we output expressions with verilog or basic syntax. E.g. arrays as [] vs ()
        self.inside_verilog_str = False
        
    # algorithm:
    # foreach variable 
    # if any predicessors bit is set
    # perform action on my variables 
    # clear my bits 
    # set my line bits:
    # if there is a test: Set taken bit or regular (not taken bit)
    # 
                
    # Run it
    def run(self):
        self.vars = {}            # All variables
        self.lists = {}            # List variables
        self.tables = {}            # Tables
        self.loops = []            # Currently active loops
        self.loopend = {}            # Mapping saying where loops end
        self.looptarget = {}        # Mapping saying next line loops target
        self.gosub = None           # Gosub return point (if any)
        self.error = 0              # Indicates program error

        self.stat = list(self.prog)  # Ordered list of all line numbers
        self.stat.sort()
        self.pc = 0                  # Current program counter
        
        # Processing prior to running
        self.collect_data()          # Collect all of the data statements
        self.check_end()             # check for the END statement 
        self.check_loops()           # check if loops are sane 

        self.output_verilog()        # output the verilog 

        if self.error:
            raise RuntimeError

        if (self.program_args['run'] == False):
            return 

        while 1:
            line = self.stat[self.pc]
            instr = self.prog[line]

            op = instr[0]

            # END and STOP statements
            if op == 'END' or op == 'STOP':
                break           # We're done
        

            # GOTO statement
            elif op == 'GOTO':
                newline = instr[1]
                self.goto(newline)
                continue

            # PRINT statement
            elif op == 'PRINT':
                plist = instr[1]
                out = ""
                for label, val in plist:
                    if out:
                        out += ' ' * (15 - (len(out) % 15))
                    out += label
                    if val:
                        if label:
                            out += " "
                        eval = self.eval(val)
                        out += str(eval)
                sys.stdout.write(out)
                end = instr[2]
                if not (end == ',' or end == ';'):
                    sys.stdout.write("\n")
                if end == ',':
                    sys.stdout.write(" " * (15 - (len(out) % 15)))
                if end == ';':
                    sys.stdout.write(" " * (3 - (len(out) % 3)))

            # LET statement
            elif op == 'LET':
                target = instr[1]
                value = instr[2]
                self.assign(target, value)

            # READ statement
            elif op == 'READ':
                for target in instr[1]:
                    if self.dc < len(self.data):
                        value = ('NUM', self.data[self.dc])
                        self.assign(target, value)
                        self.dc += 1
                    else:
                        # No more data.  Program ends
                        return
            elif op == 'IF':
                relop = instr[1]
                newline = instr[2]
                if (self.releval(relop)):
                    self.goto(newline)
                    continue

            elif op == 'FOR':
                loopvar = instr[1]
                initval = instr[2]
                finval = instr[3]
                stepval = instr[4]

                # Check to see if this is a new loop
                if not self.loops or self.loops[-1][0] != self.pc:
                    # Looks like a new loop. Make the initial assignment
                    newvalue = initval
                    self.assign((loopvar, None, None), initval)
                    if not stepval:
                        stepval = ('NUM', 1)
                    stepval = self.eval(stepval)    # Evaluate step here
                    self.loops.append((self.pc, stepval))
                else:
                    # It's a repeat of the previous loop
                    # Update the value of the loop variable according to the
                    # step
                    stepval = ('NUM', self.loops[-1][1])
                    newvalue = (
                        'BINOP', '+', ('VAR', (loopvar, None, None)), stepval)

                if self.loops[-1][1] < 0:
                    relop = '>='
                else:
                    relop = '<='
                if not self.releval(('RELOP', relop, newvalue, finval)):
                    # Loop is done. Jump to the NEXT
                    self.pc = self.loopend[self.pc]
                    self.loops.pop()
                else:
                    self.assign((loopvar, None, None), newvalue)

            elif op == 'NEXT':
                if not self.loops:
                    print("NEXT WITHOUT FOR AT LINE %s" % line)
                    return

                nextvar = instr[1]
                self.pc = self.loops[-1][0]
                loopinst = self.prog[self.stat[self.pc]]
                forvar = loopinst[1]
                if nextvar != forvar:
                    print("NEXT DOESN'T MATCH FOR AT LINE %s" % line)
                    return
                continue
            elif op == 'GOSUB':
                newline = instr[1]
                if self.gosub:
                    print("ALREADY IN A SUBROUTINE AT LINE %s" % line)
                    return
                self.gosub = self.stat[self.pc]
                self.goto(newline)
                continue

            elif op == 'RETURN':
                if not self.gosub:
                    print("RETURN WITHOUT A GOSUB AT LINE %s" % line)
                    return
                self.goto(self.gosub)
                self.gosub = None

            elif op == 'FUNC':
                fname = instr[1]
                pname = instr[2]
                expr = instr[3]

                def eval_func(pvalue, name=pname, self=self, expr=expr):
                    self.assign((pname, None, None), pvalue)
                    return self.eval(expr)
                self.functions[fname] = eval_func

            elif op == 'DIM':
                for vname, x, y in instr[1]:
                    if y == 0:
                        # Single dimension variable
                        self.lists[vname] = [0] * x
                    else:
                        # Double dimension variable
                        temp = [0] * y
                        v = []
                        for i in range(x):
                            v.append(temp[:])
                        self.tables[vname] = v

            self.pc += 1

    # Utility functions for program listing
    def expr_str(self, expr):
        etype = expr[0]

        if etype == 'NUM':
            return str(expr[1])
        elif etype == 'GROUP':
            return "(%s)" % self.expr_str(expr[1])
        elif etype == 'UNARY':
            if expr[1] == '-':
                return "-" + self.expr_str(expr[2])
            elif expr[1] == '~':
                return "~" + self.expr_str(expr[2])
            elif expr[1] == 'NOT':
                return "!" + self.expr_str(expr[2])

        elif etype == 'BINOP':
            global inside_relational_expression            
            if ( (expr[1] == '=') and inside_relational_expression == True) :
                return "%s %s %s" % (self.expr_str(expr[2]), "==", self.expr_str(expr[3]))
            elif (expr[1] == 'AND'): 
                return "%s %s %s" % (self.expr_str(expr[2]), '&&', self.expr_str(expr[3]))
            elif (expr[1] == 'OR'): 
                return "%s %s %s" % (self.expr_str(expr[2]), '||', self.expr_str(expr[3]))
            elif (expr[1] == 'NOT'):             
                return "%s %s %s" % (self.expr_str(expr[2]), '!', self.expr_str(expr[3]))
            elif (expr[1] == '<>'):             
                return "%s %s %s" % (self.expr_str(expr[2]), '!=', self.expr_str(expr[3]))            
            else:
                return "%s %s %s" % (self.expr_str(expr[2]), expr[1], self.expr_str(expr[3]))                
        elif etype == 'VAR':
            if (self.inside_verilog_str == True):
                return self.verilog_var_str(expr[1])
            else:
                return self.var_str(expr[1])
        
    def relexpr_str(self, expr):
        global inside_relational_expression
        etype = expr[0]

        if etype == 'UNARY':
            if expr[1] == 'NOT':
                return "!" + self.expr_str(expr[2])
            else:
                print "error unknown relative expression unary operator"

        if etype == 'GROUP':
            return "(%s)" % self.expr_str(expr[1])
        
        if ( (expr[1] == '=') and (inside_relational_expression == True)) :
            return "%s %s %s" % (self.expr_str(expr[2]), "==", self.expr_str(expr[3]))
        elif (expr[1] == 'AND'): 
            return "%s %s %s" % (self.expr_str(expr[2]), '&&', self.expr_str(expr[3]))
        elif (expr[1] == 'OR'): 
            return "%s %s %s" % (self.expr_str(expr[2]), '||', self.expr_str(expr[3]))
        elif (expr[1] == 'NOT'):             
            return "%s %s %s" % (self.expr_str(expr[2]), '!', self.expr_str(expr[3]))
        elif (expr[1] == '<>'):             
                return "%s %s %s" % (self.expr_str(expr[2]), '!=', self.expr_str(expr[3]))            
        else:
            return "%s %s %s" % (self.expr_str(expr[2]), expr[1], self.expr_str(expr[3]))            

    def var_str(self, var):
        varname, dim1, dim2 = var
        if not dim1 and not dim2:
            return varname
        if dim1 and not dim2:
            return "%s(%s)" % (varname, self.expr_str(dim1))
        return "%s(%s,%s)" % (varname, self.expr_str(dim1), self.expr_str(dim2))

    def verilog_var_str(self, var):
        varname, dim1, dim2 = var
        if not dim1 and not dim2:
            return varname

        if dim1 and not dim2:  # this is a hack to support HEX conversion in basic 
            if (varname == 'TOHEX') or (varname == 'INT'):  # TOHEX just strips the var out 
                return '('+self.expr_str(dim1)+')'            # also for INT, as these are all ints 
            elif (varname == 'FROMHEX'):   #FROMHEX adds the verilog hex formating for literals
                if (dim1[0] == 'NUM'):
                    return ("\'h" + self.expr_str(dim1))
                else:
                    return self.expr_str(dim1)
            else:
                return "%s[%s]" % (varname, self.expr_str(dim1))
        return "%s[%s][%s]" % (varname, self.expr_str(dim1), self.expr_str(dim2))

    # Create a program listing
    def list(self):
        stat = list(self.prog)      # Ordered list of all line numbers
        stat.sort()
        for line in stat:
            instr = self.prog[line]
            op = instr[0]
            if op in ['END', 'STOP', 'RETURN']:
                print("%s %s" % (line, op))
                continue
            elif op == 'REM':
                print("%s %s" % (line, instr[1]))
            elif op == 'PRINT':
                _out = "%s %s " % (line, op)
                first = 1
                for p in instr[1]:
                    if not first:
                        _out += ", "
                    if p[0] and p[1]:
                        _out += '"%s"%s' % (p[0], self.expr_str(p[1]))
                    elif p[1]:
                        _out += self.expr_str(p[1])
                    else:
                        _out += '"%s"' % (p[0],)
                    first = 0
                if instr[2]:
                    _out += instr[2]
                print(_out)
            elif op == 'LET':
                print("%s LET %s = %s" %
                      (line, self.var_str(instr[1]), self.expr_str(instr[2])))
            elif op == 'READ':
                _out = "%s READ " % line
                first = 1
                for r in instr[1]:
                    if not first:
                        _out += ","
                    _out += self.var_str(r)
                    first = 0
                print(_out)
            elif op == 'IF':
                print("%s IF %s THEN %d" %
                      (line, self.relexpr_str(instr[1]), instr[2]))
            elif op == 'GOTO' or op == 'GOSUB':
                print("%s %s %s" % (line, op, instr[1]))
            elif op == 'FOR':
                _out = "%s FOR %s = %s TO %s" % (
                    line, instr[1], self.expr_str(instr[2]), self.expr_str(instr[3]))
                if instr[4]:
                    _out += " STEP %s" % (self.expr_str(instr[4]))
                print(_out)
            elif op == 'NEXT':
                print("%s NEXT %s" % (line, instr[1]))
            elif op == 'FUNC':
                print("%s DEF %s(%s) = %s" %
                      (line, instr[1], instr[2], self.expr_str(instr[3])))
            elif op == 'DIM':
                _out = "%s DIM " % line
                first = 1
                for vname, x, y in instr[1]:
                    if not first:
                        _out += ","
                    first = 0
                    if y == 0:
                        _out += "%s(%d)" % (vname, x)
                    else:
                        _out += "%s(%d,%d)" % (vname, x, y)

                print(_out)
            elif op == 'DATA':
                _out = "%s DATA " % line
                first = 1
                for v in instr[1]:
                    if not first:
                        _out += ","
                    first = 0
                    _out += v
                print(_out)

    # Erase the current program
    def new(self):
        self.prog = {}

    # Insert statements
    def add_statements(self, prog):
        for line, stat in prog.items():
            self.prog[line] = stat

    # Delete a statement
    def del_line(self, lineno):
        try:
            del self.prog[lineno]
        except KeyError:
            pass
