5 REM TEST VARIOUS BASIC BITWISE AND GOSUB OPERATORS
10 LET X = 1
15 DIM D(5)
15 DIM E(5,3)
20 LET Y = 8
35 LET X = 1
30 LET Z = X << Y
40 LET Q = Y >> X
50 LET M = (X << 4) | Y
70 LET H = Y
75 LET B = 14
77 LET E(2,2) = B
78 LET D(1) = E(2,2)
80 PRINT "Z is ", Z , " hello ", M, "Q is :", Q, " D[1] is ",D(1)
90 FOR I = 1 TO 10 STEP 3
105 PRINT "I is ",I 
110 NEXT I
115 IF I < 2 THEN 200 
120 LET I = 10
125 GOTO 200 
130 PRINT " inside gosub before shift H is", H
135 LET H = (H << 1) 
137 PRINT " inside gosub H is: ", H
138 PRINT " second gosub X is: ", X
140 RETURN
200 REM example of using a subroutine
210 GOSUB 130
220 PRINT "outside and H is: ",H
230 LET X = 100
240 LET Y = 17
250 LET Q = X % Y
255 GOSUB 138
260 PRINT "X IS ",X,"Y IS",Y,"X MOD Y is: ",Q, " Q mod 7 is: ", (Q % 7)
300 END

