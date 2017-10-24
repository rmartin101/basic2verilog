module basic();
 	 
 // -------- Variable Section  ----------
 // --- User Variables ---- 
 	 reg signed [31:0] A [0:10]  ;
 	 reg signed [31:0] I ;
 	 reg signed [31:0] Y ;
 // --- Control Bits ---- 
 	 reg clk ; 
 	 reg [63:0] cycle_count ; 
 	 reg c_bit_00000_start ; 
 	 reg c_bit_00010_dim ; 
 	 reg c_bit_00020_00_assign ; 
 	 reg c_bit_00020_01_bubble ; 
 	 reg c_bit_00030_00_assign ; 
 	 reg c_bit_00030_01_bubble ; 
 	 reg c_bit_00030_02_test_taken ; 
 	 reg c_bit_00030_02_test ; 
 	 reg c_bit_00040_00_assign ; 
 	 reg c_bit_00040_01_bubble ; 
 	 reg c_bit_00050_print ; 
 	 reg c_bit_00060_00_test_taken ; 
 	 reg c_bit_00060_00_test ; 
 	 reg c_bit_00060_01_assign ; 
 	 reg c_bit_00060_02_bubble ; 
 	 reg c_bit_00070_end ; 
 // -------- Initialization Section  ----------
 initial begin 
 	 clk =0 ; 
 	 cycle_count =0 ; 
 	 c_bit_00000_start = 1 ; 
end // initial 
 // -------- Data Flow Section  ----------
always @(posedge clk) begin // dataflow for variable A 
 	  	 if (c_bit_00040_00_assign == 1) begin 
 	 	 A[I] <= I + I ; 
  	 end 
 	 else 
	 begin 
 	 	 
 	 end
 
end 
 
always @(posedge clk) begin // dataflow for variable I 
 	  	 if (c_bit_00030_00_assign == 1) begin 
 	 	 	 	 I <= 1 ; 
  	 end 
 	 else 
	 if (c_bit_00060_01_assign == 1) begin 
 	 	  I <= I + 1 ; 
  	 end 
 	 else 
	 begin 
 	 	 I <= I ; 
 	 end
 
end 
 
always @(posedge clk) begin // dataflow for variable Y 
 	  	 if (c_bit_00020_00_assign == 1) begin 
 	 	 Y <= 1 ; 
  	 end 
 	 else 
	 begin 
 	 	 Y <= Y ; 
 	 end
 
end 
 
 // -------- I/O Section  ----------
always @(posedge clk) begin 
 	  if (c_bit_00050_print == 1) begin 
 	 	 	 	 $display("%0s%0d%0s%0d","A:",I," is: ",A[I]); 
 	 end 
 	 
end 
 
 // -------- Control Flow Section  ----------
always @(posedge clk) begin // control for line 00010_dim 
 	 if ( (c_bit_00000_start == 1) ) begin 
	 c_bit_00000_start <= 0;   	 	 c_bit_00010_dim <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00010_dim <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00020_00_assign 
 	 if ( (c_bit_00010_dim == 1) ) begin 
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
 
always @(posedge clk) begin // control for line 00030_02_test 
 	 if ( (c_bit_00030_01_bubble == 1) ) begin 
	 	 if ( (1) > 0 ) begin 
	 	 	 if ( (I) > 10) begin 
 	 	 	 	 c_bit_00030_02_test_taken <= 1 ; c_bit_00030_02_test <=0 ; 
 	 	 	 end // loop exit, taken
 	 	 	 else begin 
 	 	 	 	 c_bit_00030_02_test_taken <= 0; c_bit_00030_02_test <= 1; 
 	 	 	 end 
	 	 end else begin
	 	 	 if ( (I) < 10) begin 
 	 	 	 	 c_bit_00030_02_test_taken <= 1 ; c_bit_00030_02_test <= 0 ; 
 	 	 	 	 end // loop exit, taken
 	 	 	 else begin 
 	 	 	 	 c_bit_00030_02_test_taken <= 0; c_bit_00030_02_test <= 1; 
 	 	 	 end 
 	 	 end  
 	 end 
 	 else begin 
 	 	 c_bit_00030_02_test <= 0; c_bit_00030_02_test_taken <=0 ; 
 	 end 
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00040_00_assign 
 	 if ( (c_bit_00030_02_test == 1) || (c_bit_00060_02_bubble == 1) ) begin 
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
 
always @(posedge clk) begin // control for line 00050_print 
 	 if ( (c_bit_00040_01_bubble == 1) ) begin 
 	 	 c_bit_00050_print <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00050_print <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00060_00_test 
 	 if ( (c_bit_00050_print == 1) ) begin 
	 	 if ( (1) > 0 ) begin 
	 	 	 if ( (I + 1) > 10) begin 
 	 	 	 	 c_bit_00060_00_test_taken <= 1 ; c_bit_00060_00_test <=0 ; 
 	 	 	 end // loop exit, taken
 	 	 	 else begin 
 	 	 	 	 c_bit_00060_00_test_taken <= 0; c_bit_00060_00_test <= 1; 
 	 	 	 end 
	 	 end else begin
	 	 	 if ( (I + 1) < 10) begin 
 	 	 	 	 c_bit_00060_00_test_taken <= 1 ; c_bit_00060_00_test <= 0 ; 
 	 	 	 	 end // loop exit, taken
 	 	 	 else begin 
 	 	 	 	 c_bit_00060_00_test_taken <= 0; c_bit_00060_00_test <= 1; 
 	 	 	 end 
 	 	 end  
 	 end 
 	 else begin 
 	 	 c_bit_00060_00_test <= 0; c_bit_00060_00_test_taken <=0 ; 
 	 end 
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00060_01_assign 
 	 if ( (c_bit_00060_00_test == 1) ) begin 
 	 	 c_bit_00060_01_assign <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00060_01_assign <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00060_02_bubble 
 	 if ( (c_bit_00060_01_assign == 1) ) begin 
 	 	 c_bit_00060_02_bubble <= 1 ;  
 	 end 
 	 else  begin 
 	 	 c_bit_00060_02_bubble <= 0 ; 
 	 end
end // end @ posedge clk 
 
always @(posedge clk) begin // control for line 00070_end 
 	 if ( (c_bit_00070_end == 1) || (c_bit_00060_00_test_taken == 1) ) begin 
 	 	 c_bit_00070_end <= 1 ; $finish; 
 	 end 
 	 else  begin 
 	 	 c_bit_00070_end <= 0 ; 
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
 
