
.PHONY: all

.PHONY: clean

.SUFFIXES: .bas .v .vvp

BASIC = ../src/basveri.py

# Note: multi-dimensional arrays require iverilog version 10
VERILOG = /usr/local/bin/iverilog
VPP = /usr/local/bin/vvp

PROGS = array.v dim3.v bitwise.v array.vvp dim3.vvp bitwise.vvp 

all: $(PROGS)

%.v : %.bas
	$(BASIC) -i $< -o $@

%.vvp : %.v
	 $(VERILOG)  -o $@ $<

clean:
	rm -f *.v *.vvp
