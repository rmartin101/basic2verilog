10 LET KEYLEN = 32
20 LET WORDLEN = 4
31 LET MAGICP = 3084996963
32 LET MAGICQ = 2654435769
40 DIM TEMPKEY(8)
50 DIM KEY(32)
51 DIM SUBKEY(26)
60 GOSUB 1600
70 FOR I = 32 TO 1 STEP -1
71 REM PRINT INT(I/WORDLEN)
80 LET TEMPKEY(INT((I-1)/WORDLEN)+1) = ((TEMPKEY(INT((I-1)/WORDLEN)+1) << 8) + KEY(I))
90 NEXT I
100 LET SUBKEY(1) = MAGICP
110 FOR J = 2 TO 26
120 LET SUBKEY(J) = (SUBKEY((J-1)) + MAGICQ)
122 REM PRINT SUBKEY(J)
130 NEXT J
140 LET I = 1
150 LET J = 1
160 LET A = 0
170 LET B = 0
180 FOR Z = 1 TO 26*3 STEP 1
181 LET TOSHIFT = SUBKEY(I) + A + B
182 LET SHIFTBY = 3
183 GOSUB 10000
184 LET SUBKEY(I) = ROTLRET
185 REM PRINT Z
200 LET A = SUBKEY(I)
201 REM PRINT A
202 LET TOSHIFT = TEMPKEY(J) + A + B
203 LET SHIFTBY = (A+B)%32
204 GOSUB 10000
205 LET TEMPKEY(J) = ROTLRET
220 LET B = TEMPKEY(J)
221 REM PRINT B
222 REM PRINT I, J
230 LET I =(I)%26 +1
240 LET J  = (J)%8 +1

250 NEXT Z
251 FOR I = 1 TO 26 
252 PRINT SUBKEY(I)
253 NEXT I
260 GOTO 5080


1600 LET KEY(1) = 1
1700 LET KEY(2) = 3
1800 LET KEY(3) = 2
1900 LET KEY(4) = 5 
2000 LET KEY(5) = 6 
2100 LET KEY(6) = 0 
2200 LET KEY(7) = 2 
2300 LET KEY(8) = 4 
2400 LET KEY(9) = 8
2500 LET KEY(10) = 9
2600 LET KEY(11) = 1
2700 LET KEY(12) = 5
2800 LET KEY(13) = 6
2900 LET KEY(14) = 3
3000 LET KEY(15) = 7
3100 LET KEY(16) = 4
3200 LET KEY(17) = 1
3300 LET KEY(18) = 4
3400 LET KEY(19) = 1
3500 LET KEY(20) = 2
3600 LET KEY(21) = 8
3700 LET KEY(22) = 3 
3800 LET KEY(23) = 0
3900 LET KEY(24) = 6
4000 LET KEY(25) = 8
4010 LET KEY(26) = 3
4020 LET KEY(27) = 4
4030 LET KEY(28) = 5
4040 LET KEY(29) = 5
4050 LET KEY(30) = 5
4060 LET KEY(31) = 5
4070 LET KEY(32) = 5
4080 RETURN

5080 LET FIRSTHALF = 129
5090 LET SECONDHALF = 129
5091 PRINT "Input: ",FIRSTHALF, " ", SECONDHALF
5100 LET A = FIRSTHALF + SUBKEY(1)
5200 LET B = SECONDHALF + SUBKEY(2)
5250 LET R = 12
5300 FOR I = 1 TO R
5310 LET XORAB = A^B
5311 LET TOSHIFT = XORAB
5312 LET SHIFTBY = B%32
5313 GOSUB 10000
5314 LET ASHIFTED = ROTLRET
5400 LET A = (ASHIFTED + SUBKEY(I+I+1))
5401 LET TOSHIFT = A^B
5402 LET SHIFTBY = A%32
5403 GOSUB 10000
5404 LET BSHIFTED = ROTLRET
5500 LET B = (BSHIFTED + SUBKEY(I+I+2))

5600 NEXT I
5610 PRINT "Encrypted:    ", A, " ", B


6720 FOR I = R TO 1 STEP -1
6721 LET TOSHIFT = B - SUBKEY(I+I+2)
6722 LET SHIFTBY = A%32
6723 GOSUB 20000
6724 LET BSHIFTED = ROTRRET
6900 LET B = (BSHIFTED ^ A)
6901 LET TOSHIFT = A - SUBKEY(I+I+1)
6902 LET SHIFTBY = B%32
6903 GOSUB 20000
6904 LET ASHIFTED = ROTRRET
7100 LET A = (ASHIFTED ^ B)
7110 NEXT I
7120 LET SECONDHALF = B - SUBKEY(2)
7130 LET FIRSTHALF = A - SUBKEY(1)
7131 PRINT "Decrypted:    ", FIRSTHALF, " ", SECONDHALF
7132 GOTO 50000

10000 REM ROTL
10001 LET ROTLRET = TOSHIFT
10010 FOR ZB = 1 TO SHIFTBY STEP 1
10011 LET RS = (TOSHIFT&2147483647)<<1
10012 LET LS = (TOSHIFT)&2147483648
10014 LET TOSHIFT = RS + (LS >> 31)
10030 NEXT ZB
10031 LET ROTLRET = TOSHIFT
10040 RETURN

20000 REM ROTR
20001 LET ROTRRET = TOSHIFT
20010 FOR ZB = 1 TO SHIFTBY STEP 1
20020 LET TOSHIFT = (TOSHIFT >> 1) | (TOSHIFT << 31)
20030 NEXT ZB
20031 LET ROTRRET = TOSHIFT
20040 RETURN



50000 END


