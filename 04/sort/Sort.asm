// This file is part of nand2tetris, as taught in The Hebrew University,
// and was written by Aviv Yaish, and is published under the Creative 
// Common Attribution-NonCommercial-ShareAlike 3.0 Unported License 
// https://creativecommons.org/licenses/by-nc-sa/3.0/

// An implementation of a sorting algorithm. 
// An array is given in R14 and R15, where R14 contains the start address of the 
// array, and R15 contains the length of the array. 
// You are not allowed to change R14, R15.
// The program should sort the array in-place and in descending order - 
// the largest number at the head of the array.
// You can assume that each array value x is between -16384 < x < 16384.
// You can assume that the address in R14 is at least >= 2048, and that 
// R14 + R15 <= 16383. 
// No other assumptions can be made about the length of the array.
// You can implement any sorting algorithm as long as its runtime complexity is 
// at most C*O(N^2), like bubble-sort. 

// Put your code here.
// set i =0 
	@i
	M=0

//the first loop
(MAINLOOP)

// set j = 0
	@j
	M=0


 // check if len - i <=  0
	@i
	D=M
	@R15
	D=D-M
	@END
	D;JEQ
	@INNERLOOP
	D;JMP


//the inner loop
(INNERLOOP)

// check if len - j - i ==  0
	@R15
	D=M-1
	@i
	D=D-M
	@j
	D=D-M
	@INEND
	D;JEQ
	
 //check if arr[j]<arr[j+1]

  // set D = arr[j]


	@R14
	D=M
	@j
	A=D+M
	D=M

 //check if arr[j] - arr[j+1] <= 0
	A=A+1 
	D=D-M
	@SWAP
	D;JLT

// set j += 1
	@j
	M=M+1
	@INNERLOOP
	D;JMP



(SWAP)

	@R14
	D=M
	@j
	A=D+M
	D=A 
	@addrressj
	M=D
	@addrressj
	A=M
	D=M
	@arrj
	M=D
	
	@R14
	D=M
	@j
	A=D+M 
	D=A+1 
	@addrressjp1
	M=D
	@addrressjp1
	A=M
	D=M
	@arrjp1
	M=D
	
	@arrjp1
	D=M
	@addrressj
	A=M
	M=D
	
	@arrj
	D=M
	@addrressjp1
	A=M
	M=D
	
	//j=j+1
	@j
	M=M+1
	
	@INNERLOOP
	D;JMP
	



//end of inner loop
(INEND)
	//set i+=1
	@i
	M=M+1
	
	@MAINLOOP
	D;JMP



(END)
	@END
	0;JMP