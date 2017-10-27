module basic();
 	 
 // -------- Variable Section  ----------
 // --- User Variables ---- 
 	 reg signed [31:0] B ;
 	 reg signed [31:0] D ;
 	 reg signed [31:0] E [0:5]  [0:3]  ;
 	 reg signed [31:0] H ;
 	 reg signed [31:0] I ;
 	 reg signed [31:0] M ;
 	 reg signed [31:0] Q ;
 	 reg signed [31:0] X ;
 	 reg signed [31:0] Y ;
 	 reg signed [31:0] Z ;
 // --- Control Bits ---- 
 	 reg clk ; 
 	 reg [63:0] cycle_count ; 
 	 reg c_bit_00000_start ; 
 	 reg c_bit_00005_bubble ; 
 	 reg c_bit_00010_00_assign ; 
 	 reg c_bit_00010_01_bubble ; 
 	 reg c_bit_00015_dim ; 
 	 reg c_bit_00020_00_assign ; 
 	 reg c_bit_00020_01_bubble ; 
 	 reg c_bit_00030_00_assign ; 
 	 reg c_bit_00030_01_bubble ; 
 	 reg c_bit_00035_00_assign ; 
 	 reg c_bit_00035_01_bubble ; 
 	 reg c_bit_00040_00_assign ; 
 	 reg c_bit_00040_01_bubble ; 
 	 reg c_bit_00050_00_assign ; 
 	 reg c_bit_00050_01_bubble ; 
 	 reg c_bit_00070_00_assign ; 
 	 reg c_bit_00070_01_bubble ; 
 	 reg c_bit_00075_00_assign ; 
 	 reg c_bit_00075_01_bubble ; 
 	 reg c_bit_00077_00_assign ; 
 	 reg c_bit_00077_01_bubble ; 
 	 reg c_bit_00078_00_assign ; 
 	 reg c_bit_00078_01_bubble ; 
 	 reg c_bit_00080_print ; 
 	 reg c_bit_00090_00_assign ; 
 	 reg c_bit_00090_01_bubble ; 
 	 reg c_bit_00090_02_test_taken ; 
 	 reg c_bit_00090_02_test ; 
 	 reg c_bit_00105_print ; 
 	 reg c_bit_00110_00_test_taken ; 
 	 reg c_bit_00110_00_test ; 
 	 reg c_bit_00110_01_assign ; 
 	 reg c_bit_00110_02_bubble ; 
 	 reg c_bit_00115_test_taken ; 
 	 reg c_bit_00115_test ; 
 	 reg c_bit_00120_00_assign ; 
 	 reg c_bit_00120_01_bubble ; 
 	 reg c_bit_00125_bubble ; 
 	 reg c_bit_00130_print ; 
 	 reg c_bit_00135_00_assign ; 
 	 reg c_bit_00135_01_bubble ; 
 	 reg c_bit_00137_print ; 
 	 reg c_bit_00138_print ; 
 	 reg c_bit_00140_return_gosub_00210_gosub ; 
 	 reg c_bit_00140_return_00220_print ; 
 	 reg c_bit_00140_return_gosub_00255_gosub ; 
 	 reg c_bit_00140_return_00260_print ; 
 	 reg c_bit_00200_bubble ; 
 	 reg c_bit_00210_gosub_return ; 
 	 reg c_bit_00210_gosub ; 
 	 reg c_bit_00220_print ; 
 	 reg c_bit_00230_00_assign ; 
 	 reg c_bit_00230_01_bubble ; 
 	 reg c_bit_00240_00_assign ; 
 	 reg c_bit_00240_01_bubble ; 
 	 reg c_bit_00250_00_assign ; 
 	 reg c_bit_00250_01_bubble ; 
 	 reg c_bit_00255_gosub_return ; 
 	 reg c_bit_00255_gosub ; 
 	 reg c_bit_00260_print ; 
 	 reg c_bit_00300_end ; 
 // -------- Initialization Section  ----------
 initial begin 
 	 clk =0 ; 
 	 cycle_count =0 ; 
 	 c_bit_00000_start = 1 ; 
end // initial 
 // -------- Data Flow Section  ----------
always @(posedge clk) begin // dataflow for variable B 
 	  	 if (c_bit_00075_00_assign == 1) begin 
 	 	 B <= 14 ; 
  	 end 
 	 else 
	 begin 
 	 	 B <= B ; 
 	 end
 
end 
 
always @(posedge clk) begin // dataflow for variable D 
 	  	 if (c_bit_00078_00_assign == 1) begin 
 	 	 D[1] <= E[2][2] ; 
  	 end 
 	 else 
	 begin 
 	 	 D <= D ; 
 	 end
 
end 
 
always @(posedge clk) begin // dataflow for variable E 
 	  	 if (c_bit_00077_00_assign == 1) begin 
 	 	 E[2][2] <= B ; 
  	 end 
 	 else 
	 begin 
 	 	 
 	 end
 
end 
 
always @(posedge clk) begin // dataflow for variable H 
 	  	 if (c_bit_00070_00_assign == 1) begin 
 	 	 H <= Y ; 
  	 end 
 	 else 
	 if (c_bit_00135_00_assign == 1) begin 
 	 	 H <= (H << 1) ; 
  	 end 
 	 else 
	 begin 
 	 	 H <= H ; 
 	 end
 
end 
 
always @(posedge clk) begin // dataflow for variable I 
 	  	 if (c_bit_00090_00_assign == 1) begin 
 	 	 	 	 I <= 1 ; 
  	 end 
 	 else 
	 if (c_bit_00110_01_assign == 1) begin 
 	 	  I <= I + 3 ; 
  	 end 
 	 else 
	 if (c_bit_00120_00_assign == 1) begin 
 	 	 I <= 10 ; 
  	 end 
 	 else 
	 begin 
 	 	 I <= I ; 
 	 end
 
end 
 
always @(posedge clk) begin // dataflow for variable M 
 	  	 if (c_bit_00050_00_assign == 1) begin 
 	 	 M <= (X << 4) | Y ; 
  	 end 
 	 else 
	 begin 
 	 	 M <= M ; 
 	 end
 
end 
 
always @(posedge clk) begin // dataflow for variable Q 
 	  	 if (c_bit_00040_00_assign == 1) begin 
 	 	 Q <= Y >> X ; 
  	 end 
 	 else 
	 if (c_bit_00250_00_assign == 1) begin 
 	 	 Q <= X % Y ; 
  	 end 
 	 else 
	 begin 
 	 	 Q <= Q ; 
 	 end
 
end 
 
always @(posedge clk) begin // dataflow for variable X 
 	  	 if (c_bit_00010_00_assign == 1) begin 
 	 	 X <= 1 ; 
  	 end 
 	 else 
	 if (c_bit_00035_00_assign == 1) begin 
 	 	 X <= 1 ; 
  	 end 
 	 else 
	 if (c_bit_00230_00_assign == 1) begin 
 	 	 X <= 100 ; 
  	 end 
 	 else 
	 begin 
 	 	 X <= X ; 
 	 end
 
end 
 
always @(posedge clk) begin // dataflow for variable Y 
 	  	 if (c_bit_00020_00_assign == 1) begin 
 	 	 Y <= 8 ; 
  	 end 
 	 else 
	 if (c_bit_00240_00_assign == 1) begin 
 	 	 Y <= 17 ; 
  	 end 
 	 else 
	 begin 
 	 	 Y <= Y ; 
 	 end
 
end 
 
always @(posedge clk) begin // dataflow for variable Z 
 	  	 if (c_bit_00030_00_assign == 1) begin 
 	 	 Z <= X << Y ; 
  	 end 
 	 else 
	 begin 
 	 	 Z <= Z ; 
 	 end
 
end 
 
 // -------- I/O Section  ----------
always @(posedge clk) begin 
 	  if (c_bit_00080_print == 1) begin 
 	 	 	 	 $display("%0s%0d%0s%0d%0s%0d%0s%0d","Z is ",Z," hello ",M,"Q is :",Q," D[1] is ",D[1]); 
 	 end 
 	 
if (c_bit_00105_print == 1) begin 
 	 	 	 	 $display("%0s%0d","I is ",I); 
 	 end 
 	 
if (c_bit_00130_print == 1) begin 
 	 	 	 	 $display("%0s%0d"," inside gosub before shift H is",H); 
 	 end 
 	 
if (c_bit_00137_print == 1) begin 
 	 	 	 	 $display("%0s%0d"," inside gosub H is: ",H); 
 	 end 
 	 
if (c_bit_00138_print == 1) begin 
 	 	 	 	 $display("%0s%0d"," second gosub X is: ",X); 
 	 end 
 	 
if (c_bit_00220_print == 1) begin 
 	 	 	 	 $display("%0s%0d","outside and H is: ",H); 
 	 end 
 	 
if (c_bit_00260_print == 1) begin 
 	 	 	 	 $display("%0s%0d%0s%0d%0s%0d%0s","X IS ",X,"Y IS",Y,"X MOD Y is: ",Q," Q mod 7 is: "); 
 	 end 
 	 
end 
 
 // -------- Control Flow Section  ----------
always @(posedge clk) begin // control for line 00005_bubble 
 	 if ( (c_bit_00000_start == 1) ) begin 
	 c_bit_00000_start <= 0;   	 	 c_bit_00005_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00005_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00010_00_assign 
 	 if ( (c_bit_00005_bubble == 1) ) begin 
 	 	 c_bit_00010_00_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00010_00_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00010_01_bubble 
 	 if ( (c_bit_00010_00_assign == 1) ) begin 
 	 	 c_bit_00010_01_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00010_01_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00015_dim 
 	 if ( (c_bit_00010_01_bubble == 1) ) begin 
 	 	 c_bit_00015_dim <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00015_dim <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00020_00_assign 
 	 if ( (c_bit_00015_dim == 1) ) begin 
 	 	 c_bit_00020_00_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00020_00_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00020_01_bubble 
 	 if ( (c_bit_00020_00_assign == 1) ) begin 
 	 	 c_bit_00020_01_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00020_01_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00030_00_assign 
 	 if ( (c_bit_00020_01_bubble == 1) ) begin 
 	 	 c_bit_00030_00_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00030_00_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00030_01_bubble 
 	 if ( (c_bit_00030_00_assign == 1) ) begin 
 	 	 c_bit_00030_01_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00030_01_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00035_00_assign 
 	 if ( (c_bit_00030_01_bubble == 1) ) begin 
 	 	 c_bit_00035_00_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00035_00_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00035_01_bubble 
 	 if ( (c_bit_00035_00_assign == 1) ) begin 
 	 	 c_bit_00035_01_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00035_01_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00040_00_assign 
 	 if ( (c_bit_00035_01_bubble == 1) ) begin 
 	 	 c_bit_00040_00_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00040_00_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00040_01_bubble 
 	 if ( (c_bit_00040_00_assign == 1) ) begin 
 	 	 c_bit_00040_01_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00040_01_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00050_00_assign 
 	 if ( (c_bit_00040_01_bubble == 1) ) begin 
 	 	 c_bit_00050_00_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00050_00_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00050_01_bubble 
 	 if ( (c_bit_00050_00_assign == 1) ) begin 
 	 	 c_bit_00050_01_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00050_01_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00070_00_assign 
 	 if ( (c_bit_00050_01_bubble == 1) ) begin 
 	 	 c_bit_00070_00_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00070_00_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00070_01_bubble 
 	 if ( (c_bit_00070_00_assign == 1) ) begin 
 	 	 c_bit_00070_01_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00070_01_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00075_00_assign 
 	 if ( (c_bit_00070_01_bubble == 1) ) begin 
 	 	 c_bit_00075_00_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00075_00_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00075_01_bubble 
 	 if ( (c_bit_00075_00_assign == 1) ) begin 
 	 	 c_bit_00075_01_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00075_01_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00077_00_assign 
 	 if ( (c_bit_00075_01_bubble == 1) ) begin 
 	 	 c_bit_00077_00_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00077_00_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00077_01_bubble 
 	 if ( (c_bit_00077_00_assign == 1) ) begin 
 	 	 c_bit_00077_01_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00077_01_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00078_00_assign 
 	 if ( (c_bit_00077_01_bubble == 1) ) begin 
 	 	 c_bit_00078_00_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00078_00_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00078_01_bubble 
 	 if ( (c_bit_00078_00_assign == 1) ) begin 
 	 	 c_bit_00078_01_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00078_01_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00080_print 
 	 if ( (c_bit_00078_01_bubble == 1) ) begin 
 	 	 c_bit_00080_print <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00080_print <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00090_00_assign 
 	 if ( (c_bit_00080_print == 1) ) begin 
 	 	 c_bit_00090_00_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00090_00_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00090_01_bubble 
 	 if ( (c_bit_00090_00_assign == 1) ) begin 
 	 	 c_bit_00090_01_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00090_01_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00090_02_test 
 	 if ( (c_bit_00090_01_bubble == 1) ) begin 
	 	 if ( (3) > 0 ) begin 
	 	 	 if ( (I) > 10) begin 
 	 	 	 	 c_bit_00090_02_test_taken <= 1 ; c_bit_00090_02_test <=0 ; 
 	 	 	 end // loop exit, taken
 	 	 	 else begin 
 	 	 	 	 c_bit_00090_02_test_taken <= 0; c_bit_00090_02_test <= 1; 
 	 	 	 end 
	 	 end else begin
	 	 	 if ( (I) < 10) begin 
 	 	 	 	 c_bit_00090_02_test_taken <= 1 ; c_bit_00090_02_test <= 0 ; 
 	 	 	 	 end // loop exit, taken
 	 	 	 else begin 
 	 	 	 	 c_bit_00090_02_test_taken <= 0; c_bit_00090_02_test <= 1; 
 	 	 	 end 
 	 	 end  
 	 end 
 	 else begin 
 	 	 c_bit_00090_02_test <= 0; c_bit_00090_02_test_taken <=0 ; 
 	 end 
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00105_print 
 	 if ( (c_bit_00090_02_test == 1) || (c_bit_00110_02_bubble == 1) ) begin 
 	 	 c_bit_00105_print <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00105_print <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00110_00_test 
 	 if ( (c_bit_00105_print == 1) ) begin 
	 	 if ( (3) > 0 ) begin 
	 	 	 if ( (I + 3) > 10) begin 
 	 	 	 	 c_bit_00110_00_test_taken <= 1 ; c_bit_00110_00_test <=0 ; 
 	 	 	 end // loop exit, taken
 	 	 	 else begin 
 	 	 	 	 c_bit_00110_00_test_taken <= 0; c_bit_00110_00_test <= 1; 
 	 	 	 end 
	 	 end else begin
	 	 	 if ( (I + 3) < 10) begin 
 	 	 	 	 c_bit_00110_00_test_taken <= 1 ; c_bit_00110_00_test <= 0 ; 
 	 	 	 	 end // loop exit, taken
 	 	 	 else begin 
 	 	 	 	 c_bit_00110_00_test_taken <= 0; c_bit_00110_00_test <= 1; 
 	 	 	 end 
 	 	 end  
 	 end 
 	 else begin 
 	 	 c_bit_00110_00_test <= 0; c_bit_00110_00_test_taken <=0 ; 
 	 end 
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00110_01_assign 
 	 if ( (c_bit_00110_00_test == 1) ) begin 
 	 	 c_bit_00110_01_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00110_01_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00110_02_bubble 
 	 if ( (c_bit_00110_01_assign == 1) ) begin 
 	 	 c_bit_00110_02_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00110_02_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00115_test 
 	 if ( (c_bit_00110_00_test_taken == 1) || (c_bit_00090_02_test_taken == 1) ) begin 
 	 	 if (I < 2) begin  
 	  	 	 	 c_bit_00115_test_taken <= 1 ; c_bit_00115_test <=0 ; 
 	 	 	 end // if taken
 	 	 else begin 
 	 	 	 	 c_bit_00115_test <= 1; c_bit_00115_test_taken <= 0; end 
 	 end 
 	 else begin 
 	 	 c_bit_00115_test <= 0; c_bit_00115_test_taken <=0 ; end 
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00120_00_assign 
 	 if ( (c_bit_00115_test == 1) ) begin 
 	 	 c_bit_00120_00_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00120_00_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00120_01_bubble 
 	 if ( (c_bit_00120_00_assign == 1) ) begin 
 	 	 c_bit_00120_01_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00120_01_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00125_bubble 
 	 if ( (c_bit_00120_01_bubble == 1) ) begin 
 	 	 c_bit_00125_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00125_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00130_print 
 	 if ( (c_bit_00210_gosub == 1) ) begin 
 	 	 c_bit_00130_print <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00130_print <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00135_00_assign 
 	 if ( (c_bit_00130_print == 1) ) begin 
 	 	 c_bit_00135_00_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00135_00_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00135_01_bubble 
 	 if ( (c_bit_00135_00_assign == 1) ) begin 
 	 	 c_bit_00135_01_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00135_01_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00137_print 
 	 if ( (c_bit_00135_01_bubble == 1) ) begin 
 	 	 c_bit_00137_print <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00137_print <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00138_print 
 	 if ( (c_bit_00137_print == 1) || (c_bit_00255_gosub == 1) ) begin 
 	 	 c_bit_00138_print <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00138_print <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00140_return 
 	 if ( (c_bit_00138_print == 1) ) begin 
	 	 if (c_bit_00210_gosub_return == 1) begin 
 	 	 	 c_bit_00140_return_gosub_00210_gosub <= 1 ; 
	 	 	 c_bit_00140_return_00220_print <= 1; 
 	 	 end 
 
 	 	 else  	 	 if (c_bit_00255_gosub_return == 1) begin 
 	 	 	 c_bit_00140_return_gosub_00255_gosub <= 1 ; 
	 	 	 c_bit_00140_return_00260_print <= 1; 
 	 	 end 
 
	 end 
 	 else begin
	 	 c_bit_00140_return_gosub_00210_gosub <= 0 ; 
	 	 c_bit_00140_return_00220_print <= 0 ; 
	 	 c_bit_00140_return_gosub_00255_gosub <= 0 ; 
	 	 c_bit_00140_return_00260_print <= 0 ; 
	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00200_bubble 
 	 if ( (c_bit_00125_bubble == 1) || (c_bit_00115_test_taken == 1) ) begin 
 	 	 c_bit_00200_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00200_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00210_gosub 
 	 if ( (c_bit_00200_bubble == 1) ) begin 
 	 	 c_bit_00210_gosub  <= 1; 
 	 	 c_bit_00210_gosub_return <= 1; 
 	 end 
 	 else if (c_bit_00140_return_gosub_00210_gosub == 1) begin 
	 	 c_bit_00210_gosub_return <= 0 ; 
 	 	 c_bit_00210_gosub <= 0; 
 	 	 end 
	 else begin 
 	 	 c_bit_00210_gosub <=0 ; 
 	 	 c_bit_00210_gosub_return <= c_bit_00210_gosub_return ; 
 	 end 
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00220_print 
 	 if ( (c_bit_00140_return_00220_print == 1) ) begin 
 	 	 c_bit_00220_print <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00220_print <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00230_00_assign 
 	 if ( (c_bit_00220_print == 1) ) begin 
 	 	 c_bit_00230_00_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00230_00_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00230_01_bubble 
 	 if ( (c_bit_00230_00_assign == 1) ) begin 
 	 	 c_bit_00230_01_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00230_01_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00240_00_assign 
 	 if ( (c_bit_00230_01_bubble == 1) ) begin 
 	 	 c_bit_00240_00_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00240_00_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00240_01_bubble 
 	 if ( (c_bit_00240_00_assign == 1) ) begin 
 	 	 c_bit_00240_01_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00240_01_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00250_00_assign 
 	 if ( (c_bit_00240_01_bubble == 1) ) begin 
 	 	 c_bit_00250_00_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00250_00_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00250_01_bubble 
 	 if ( (c_bit_00250_00_assign == 1) ) begin 
 	 	 c_bit_00250_01_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00250_01_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00255_gosub 
 	 if ( (c_bit_00250_01_bubble == 1) ) begin 
 	 	 c_bit_00255_gosub  <= 1; 
 	 	 c_bit_00255_gosub_return <= 1; 
 	 end 
 	 else if (c_bit_00140_return_gosub_00255_gosub == 1) begin 
	 	 c_bit_00255_gosub_return <= 0 ; 
 	 	 c_bit_00255_gosub <= 0; 
 	 	 end 
	 else begin 
 	 	 c_bit_00255_gosub <=0 ; 
 	 	 c_bit_00255_gosub_return <= c_bit_00255_gosub_return ; 
 	 end 
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00260_print 
 	 if ( (c_bit_00140_return_00260_print == 1) ) begin 
 	 	 c_bit_00260_print <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00260_print <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00300_end 
 	 if ( (c_bit_00260_print == 1) || (c_bit_00300_end == 1) ) begin 
 	 	 c_bit_00300_end <= 1 ; $finish; 
 	 end 
 	 else  begin 
 	 	 c_bit_00300_end <= 0 ; 
 	 end
end // end @ posedge clk 
 
 // -------- Trailer Section  ----------
 	 // cycle counter
always @(posedge clk) begin
 	 if (cycle_count > 50000) begin   	 	 $display("reached maximum cycle count of 50000");
 	 	  $finish;
 	 end
 	 else begin
 	 	 cycle_count <= cycle_count + 1 ;
	 end
 end 
 
 	 // clock generator
 	 always
 	 	 #1 clk = !clk ; 
endmodule // basic
 
