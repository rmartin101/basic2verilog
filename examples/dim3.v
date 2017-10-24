module basic();
 	 
 // -------- Variable Section  ----------
 // --- User Variables ---- 
 	 reg signed [31:0] A [0:4]  [0:12]  ;
 	 reg signed [31:0] I ;
 	 reg signed [31:0] J ;
 	 reg signed [31:0] MAXX ;
 	 reg signed [31:0] MAXY ;
 // --- Control Bits ---- 
 	 reg clk ; 
 	 reg [63:0] cycle_count ; 
 	 reg c_bit_00000_start ; 
 	 reg c_bit_00005_dim ; 
 	 reg c_bit_00006_00_assign ; 
 	 reg c_bit_00006_01_bubble ; 
 	 reg c_bit_00007_00_assign ; 
 	 reg c_bit_00007_01_bubble ; 
 	 reg c_bit_00010_00_assign ; 
 	 reg c_bit_00010_01_bubble ; 
 	 reg c_bit_00010_02_test_taken ; 
 	 reg c_bit_00010_02_test ; 
 	 reg c_bit_00020_00_assign ; 
 	 reg c_bit_00020_01_bubble ; 
 	 reg c_bit_00020_02_test_taken ; 
 	 reg c_bit_00020_02_test ; 
 	 reg c_bit_00030_00_assign ; 
 	 reg c_bit_00030_01_bubble ; 
 	 reg c_bit_00035_print ; 
 	 reg c_bit_00040_00_test_taken ; 
 	 reg c_bit_00040_00_test ; 
 	 reg c_bit_00040_01_assign ; 
 	 reg c_bit_00040_02_bubble ; 
 	 reg c_bit_00050_00_test_taken ; 
 	 reg c_bit_00050_00_test ; 
 	 reg c_bit_00050_01_assign ; 
 	 reg c_bit_00050_02_bubble ; 
 	 reg c_bit_00100_end ; 
 // -------- Initialization Section  ----------
 initial begin 
 	 clk =0 ; 
 	 cycle_count =0 ; 
 	 c_bit_00000_start = 1 ; 
end // initial 
 // -------- Data Flow Section  ----------
always @(posedge clk) begin // dataflow for variable A 
 	  	 if (c_bit_00030_00_assign == 1) begin 
 	 	 A[I][J] <= I + J ; 
  	 end 
 	 else 
	 begin 
 	 	 
 	 end
 
end 
 
always @(posedge clk) begin // dataflow for variable I 
 	  	 if (c_bit_00010_00_assign == 1) begin 
 	 	 	 	 I <= 1 ; 
  	 end 
 	 else 
	 if (c_bit_00050_01_assign == 1) begin 
 	 	  I <= I + 1 ; 
  	 end 
 	 else 
	 begin 
 	 	 I <= I ; 
 	 end
 
end 
 
always @(posedge clk) begin // dataflow for variable J 
 	  	 if (c_bit_00020_00_assign == 1) begin 
 	 	 	 	 J <= 1 ; 
  	 end 
 	 else 
	 if (c_bit_00040_01_assign == 1) begin 
 	 	  J <= J + 1 ; 
  	 end 
 	 else 
	 begin 
 	 	 J <= J ; 
 	 end
 
end 
 
always @(posedge clk) begin // dataflow for variable MAXX 
 	  	 if (c_bit_00006_00_assign == 1) begin 
 	 	 MAXX <= 4 ; 
  	 end 
 	 else 
	 begin 
 	 	 MAXX <= MAXX ; 
 	 end
 
end 
 
always @(posedge clk) begin // dataflow for variable MAXY 
 	  	 if (c_bit_00007_00_assign == 1) begin 
 	 	 MAXY <= 12 ; 
  	 end 
 	 else 
	 begin 
 	 	 MAXY <= MAXY ; 
 	 end
 
end 
 
 // -------- I/O Section  ----------
always @(posedge clk) begin 
 	  if (c_bit_00035_print == 1) begin 
 	 	 	 	 $display("%0s%0d%0s%0d%0s%0d","I is: ",I," J is: ",J," A(I,J) is: ",A[I][J]); 
 	 end 
 	 
end 
 
 // -------- Control Flow Section  ----------
always @(posedge clk) begin // control for line 00005_dim 
 	 if ( (c_bit_00000_start == 1) ) begin 
	 c_bit_00000_start <= 0;   	 	 c_bit_00005_dim <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00005_dim <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00006_00_assign 
 	 if ( (c_bit_00005_dim == 1) ) begin 
 	 	 c_bit_00006_00_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00006_00_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00006_01_bubble 
 	 if ( (c_bit_00006_00_assign == 1) ) begin 
 	 	 c_bit_00006_01_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00006_01_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00007_00_assign 
 	 if ( (c_bit_00006_01_bubble == 1) ) begin 
 	 	 c_bit_00007_00_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00007_00_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00007_01_bubble 
 	 if ( (c_bit_00007_00_assign == 1) ) begin 
 	 	 c_bit_00007_01_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00007_01_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00010_00_assign 
 	 if ( (c_bit_00007_01_bubble == 1) ) begin 
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
 
always @(posedge clk) begin // control for line 00010_02_test 
 	 if ( (c_bit_00010_01_bubble == 1) ) begin 
	 	 if ( (1) > 0 ) begin 
	 	 	 if ( (I) > MAXX) begin 
 	 	 	 	 c_bit_00010_02_test_taken <= 1 ; c_bit_00010_02_test <=0 ; 
 	 	 	 end // loop exit, taken
 	 	 	 else begin 
 	 	 	 	 c_bit_00010_02_test_taken <= 0; c_bit_00010_02_test <= 1; 
 	 	 	 end 
	 	 end else begin
	 	 	 if ( (I) < MAXX) begin 
 	 	 	 	 c_bit_00010_02_test_taken <= 1 ; c_bit_00010_02_test <= 0 ; 
 	 	 	 	 end // loop exit, taken
 	 	 	 else begin 
 	 	 	 	 c_bit_00010_02_test_taken <= 0; c_bit_00010_02_test <= 1; 
 	 	 	 end 
 	 	 end  
 	 end 
 	 else begin 
 	 	 c_bit_00010_02_test <= 0; c_bit_00010_02_test_taken <=0 ; 
 	 end 
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00020_00_assign 
 	 if ( (c_bit_00010_02_test == 1) || (c_bit_00050_02_bubble == 1) ) begin 
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
 
always @(posedge clk) begin // control for line 00020_02_test 
 	 if ( (c_bit_00020_01_bubble == 1) ) begin 
	 	 if ( (1) > 0 ) begin 
	 	 	 if ( (J) > MAXY) begin 
 	 	 	 	 c_bit_00020_02_test_taken <= 1 ; c_bit_00020_02_test <=0 ; 
 	 	 	 end // loop exit, taken
 	 	 	 else begin 
 	 	 	 	 c_bit_00020_02_test_taken <= 0; c_bit_00020_02_test <= 1; 
 	 	 	 end 
	 	 end else begin
	 	 	 if ( (J) < MAXY) begin 
 	 	 	 	 c_bit_00020_02_test_taken <= 1 ; c_bit_00020_02_test <= 0 ; 
 	 	 	 	 end // loop exit, taken
 	 	 	 else begin 
 	 	 	 	 c_bit_00020_02_test_taken <= 0; c_bit_00020_02_test <= 1; 
 	 	 	 end 
 	 	 end  
 	 end 
 	 else begin 
 	 	 c_bit_00020_02_test <= 0; c_bit_00020_02_test_taken <=0 ; 
 	 end 
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00030_00_assign 
 	 if ( (c_bit_00020_02_test == 1) || (c_bit_00040_02_bubble == 1) ) begin 
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
 
always @(posedge clk) begin // control for line 00035_print 
 	 if ( (c_bit_00030_01_bubble == 1) ) begin 
 	 	 c_bit_00035_print <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00035_print <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00040_00_test 
 	 if ( (c_bit_00035_print == 1) ) begin 
	 	 if ( (1) > 0 ) begin 
	 	 	 if ( (J + 1) > MAXY) begin 
 	 	 	 	 c_bit_00040_00_test_taken <= 1 ; c_bit_00040_00_test <=0 ; 
 	 	 	 end // loop exit, taken
 	 	 	 else begin 
 	 	 	 	 c_bit_00040_00_test_taken <= 0; c_bit_00040_00_test <= 1; 
 	 	 	 end 
	 	 end else begin
	 	 	 if ( (J + 1) < MAXY) begin 
 	 	 	 	 c_bit_00040_00_test_taken <= 1 ; c_bit_00040_00_test <= 0 ; 
 	 	 	 	 end // loop exit, taken
 	 	 	 else begin 
 	 	 	 	 c_bit_00040_00_test_taken <= 0; c_bit_00040_00_test <= 1; 
 	 	 	 end 
 	 	 end  
 	 end 
 	 else begin 
 	 	 c_bit_00040_00_test <= 0; c_bit_00040_00_test_taken <=0 ; 
 	 end 
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00040_01_assign 
 	 if ( (c_bit_00040_00_test == 1) ) begin 
 	 	 c_bit_00040_01_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00040_01_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00040_02_bubble 
 	 if ( (c_bit_00040_01_assign == 1) ) begin 
 	 	 c_bit_00040_02_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00040_02_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00050_00_test 
 	 if ( (c_bit_00040_00_test_taken == 1) || (c_bit_00020_02_test_taken == 1) ) begin 
	 	 if ( (1) > 0 ) begin 
	 	 	 if ( (I + 1) > MAXX) begin 
 	 	 	 	 c_bit_00050_00_test_taken <= 1 ; c_bit_00050_00_test <=0 ; 
 	 	 	 end // loop exit, taken
 	 	 	 else begin 
 	 	 	 	 c_bit_00050_00_test_taken <= 0; c_bit_00050_00_test <= 1; 
 	 	 	 end 
	 	 end else begin
	 	 	 if ( (I + 1) < MAXX) begin 
 	 	 	 	 c_bit_00050_00_test_taken <= 1 ; c_bit_00050_00_test <= 0 ; 
 	 	 	 	 end // loop exit, taken
 	 	 	 else begin 
 	 	 	 	 c_bit_00050_00_test_taken <= 0; c_bit_00050_00_test <= 1; 
 	 	 	 end 
 	 	 end  
 	 end 
 	 else begin 
 	 	 c_bit_00050_00_test <= 0; c_bit_00050_00_test_taken <=0 ; 
 	 end 
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00050_01_assign 
 	 if ( (c_bit_00050_00_test == 1) ) begin 
 	 	 c_bit_00050_01_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00050_01_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00050_02_bubble 
 	 if ( (c_bit_00050_01_assign == 1) ) begin 
 	 	 c_bit_00050_02_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00050_02_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00100_end 
 	 if ( (c_bit_00100_end == 1) || (c_bit_00050_00_test_taken == 1) ) begin 
 	 	 c_bit_00100_end <= 1 ; $finish; 
 	 end 
 	 else  begin 
 	 	 c_bit_00100_end <= 0 ; 
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
 
