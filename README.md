# The Bonato-1, designed by me.
![The main circuit](https://github.com/MarcoBonato09/bonato-1/assets/99590461/6d87c66b-9f15-4024-96ad-1364c2dac223)

## Architecture
I would recommend downloading main.circ from this repo and checking it out yourself! Apart from that;
  - There are 8 general purpose registers, R0 to R7
  - There are the following special-purpose registers:
      - The flags register: stores results of comparison operations (for example, is Ra > Rb, or was there overflow when calculating Ra + Rb)
      - The program counter (abbreviated PC): stores the instruction address of the next instruction to be executed
      - The current instruction register (abbreviated CIR): stores the current instruction being executed. Is contained within the program loader circuit.
  - Instructions and data are stored separately. More specifically, programs are stored in ROM, in the program loader circuit.

## [The instruction set](https://docs.google.com/spreadsheets/d/1MOb1YVkWXCrEX2oYxiGSCioapgrsqMv9-_7IW9adN6s/edit?usp=sharing)
  This computer has a 24-bit instruction design, with 16-bit data. It has a 5-bit opcode, 3-bit register addressing, and 16-bit memory and instruction addressing.
  Below in bullet points are the instructions the computer can perform:
  - none
      - ignored by computer, does nothing)
  - halt
     - floors clock signal to zero. There is a restart button to re-enable the clock (see above)
  - set Rn <value>
     - sets the value of Rn to <value>
     - Example: set R1 5
     - Example 2: set R5 -3
  - copy Rn Ra
     - copies the value in Ra to Rn
     - Example: copy R5 R1
  - load Rn <memory_address>
     - sets the value of Rn to the value stored at address <memory_address> in main memory
     - Example: load R7 54
  - store Rn <memory_address>
     - sets the value of main memory at <memory_address> to the value stored in Rn
     - Example: store R2 10
  - compare Rn Ra
     - compares the values stored in Rn and Ra, storing the results in the flags register
     - Example: compare R0 R4
  - branch <condition_type> <label>
     - <condition_type> can be any one of:
        - lt (less than)
        - lte (less than or equal to)
        - eq (equal to)
        - gt (greater than)
        - gte (greater than or equal to)
        - ov (overflow from addition operation)
        - al (always branch)
        - ne (not equal to)
     - If the condition is met according to the last compare operation, the PC address is set to the instruction address of the specified label
     - Example (assuming an earlier label was created called loop): branch lt loop
  - <alu_operation> Rn Ra Rb
     - Performs a calculation specified by <alu_operation> on Ra and Rb and stores the result in Rn
     - <alu_operation> can be any one of:
         - add, subtract, divide, modulo
         - lowmul, highmul (gives the low and high bits of multiplication respectively)
         - bitwise and, or, not or xor
         - lshift, rshift, arshift (left shift, right shift, and arithmetic right shift respectively)
     - Example: add R5 R1 R2
     - Example 2: and R1 R0 R3

## Writing assembly and compiling
Please take a look at both compiler.py and the sample program that counts to 10. This gives you an idea of how to write code for my compiler to read.
The right syntax to write programs for the compiler is the same as the syntax in the example bullet points above for each instruction.

As specified in compiler.py:
  - IMPORTANT: for the reset button to work properly, the first line of code should be a label or a none instruction.
  - Source code should be in a plain text file called 'code.txt' in the same directory as compiler.py
  - The output file is called hex_code, and contains the hex version of the instructions to be imported into logisim program ROM
  - The program ROM can be found inside of the program loader circuit.
