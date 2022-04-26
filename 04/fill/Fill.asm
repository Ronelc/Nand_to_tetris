// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.


(LOOP)
// Get keyboard value, and jump to black\white.

    @KBD
    D=M
    @WHITE
    D;JEQ
    @BLACK
    0;JMP

// Paint the screen at black. 
(BLACK)
    @blackOrWhite
    M=-1
    @DRAW
    0;JMP

// Paint the screen at white
(WHITE)
    @blackOrWhite
    M=0
    @DRAW
    0;JMP

// Set the screen to the right color.
(DRAW)
    @8191
    D=A
    @counter
    M=D

// Walk the screen and set the values to the right color.
(NEXT)
        @counter
        D=M
        @pos
        M=D
        @SCREEN
        D=A
        @pos
        M=M+D

// Actually draw the value at the current position.
        @blackOrWhite
        D=M
        @pos
        A=M
        M=D

// Decrement the counter.
        @counter
        D=M-1
        M=D

// Next if the counter is still >= 0.
        @NEXT
        D;JGE

// Loop back around.
    @LOOP
    0;JMP















