100 LET X = 2
105 LET G = 0
110 GOSUB 400
120 PRINT "U is: ",U, " V IS: ", V, " W IS: ",W
200 LET X = 5
210 GOSUB 400
220 LET Z = U + 2*V + 3*W
230 PRINT "Z is ",Z
240 GOSUB 500
250 LET G = 1
400 LET U = X*X
410 LET V = X*X*X
420 LET W = X*X*X*X + X*X*X + X*X + X
425 IF G = 1 THEN 999
430 RETURN
500 LET K = W*X + ( X+3 ) + X
510 RETURN
999 END
