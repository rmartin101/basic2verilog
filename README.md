# basic2verilog

## A Basic to Verilog Compiler 

This is a first cut at a BASIC to Verilog compiler.

All files are (C) 2017, Richard P. Martin, and under the GNU General Public License, version 3,
unless otherwise noted in the source code.

The compiler is still quite rough and has bugs. You will need iverilog version 10 to
run the examples that use multi-dimensional arrays. The compiler should generate
synthesizable code.

To compile, go to the examples directory and run make.

To run, you need to execute vvp manually, as the automatic tests are not finished yet.

