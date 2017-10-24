#!/usr/bin/python

# Implementation of a basic to verilog compiler 

# This file provides the runtime support for running a basic program
# Assumes the program has been parsed using basparse.py

# built on PLY (Python L(ex Yacc) code from David M. Beazley dave@dabeaz.com
# See: https://github.com/dabeaz/ply.git

import sys
#sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

import basiclex
import basparse
import basic2verilog
import argparse

# If a filename has been specified, we try to run it.
# If a runtime error occurs, we bail out and enter
# interactive mode below

# This is the list of options:
#
# -o <filename> : output file
# -i <filename> : input file 
# -v output verilog (default) 
# -c output c (future reference) 
# -s <bits> : default number of bits for a number/integer: Default is 32
# -r :  Run the program in the basic interpreter (default does not run) 
                        
def parse_args(parser,argv):
    parser.add_argument("-o", "--output", type=str,
                        help="output filename")
    parser.add_argument("-i", "--input", type=str,
                        help="input filename")
    parser.add_argument("-r", "--run", action="store_true",
                        help="run the basic interpreter")
    parser.add_argument("-w", "--width",type=int,
                        help="bit-width of variables")
    args = parser.parse_args()
    return args


parser = argparse.ArgumentParser()
# convert the args from a namespace to a normal dictionary
if (len(sys.argv) > 2):
    namespace_args = parse_args(parser,sys.argv)
    args = vars(namespace_args)
else:
    args = {}
    
# set to run the program in the basic interpreter or not 
if (not ('run' in args) ):
    args['run'] = False 

if (not ('output' in args)):
    args['output'] = 'a.out'
    
if len(sys.argv) == 1:
    b = basic2verilog.BasicInterpreter({},args)
elif len(sys.argv) >= 2:
    if len(sys.argv) == 2:
        argv = sys.argv 
        data = open(sys.argv[1]).read()
    else:
        if (not ('input' in args)):
            print 'No input file specified'
            raise SystemExit            
        data = open(args['input']).read()
        
    prog = basparse.parse(data)
    if not prog:
        raise SystemExit
    b = basic2verilog.BasicInterpreter(prog,args)
    try:
        b.run()
        raise SystemExit
    except RuntimeError:
        pass

    
# Interactive mode.  This incrementally adds/deletes statements
# from the program stored in the BasicInterpreter object.  In
# addition, special commands 'NEW','LIST',and 'RUN' are added.
# Specifying a line number with no code deletes that line from
# the program.

while 1:
    try:
        line = raw_input("[BASIC] ")
    except EOFError:
        raise SystemExit
    if not line:
        continue
    line += "\n"
    prog = basparse.parse(line)
    if not prog:
        continue

    keys = list(prog)
    if keys[0] > 0:
        b.add_statements(prog)
    else:
        stat = prog[keys[0]]
        if stat[0] == 'RUN':
            try:
                b.run()
            except RuntimeError:
                pass
        elif stat[0] == 'LIST':
            b.list()
        elif stat[0] == 'BLANK':
            b.del_line(stat[1])
        elif stat[0] == 'NEW':
            b.new()
