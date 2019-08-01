import sys
# Main Advantages of Using a Stack
#     -Store things temporarily
#     -Also store local variables (will discuss this tomorrow)
PRINT_BEEJ      = 1
HALT            = 2
PRINT_NUM       = 3
SAVE_REGISTER   = 4
PRINT_REGISTER  = 5
PUSH            = 6
POP             = 7
CALL            = 8
RET             = 9
memory = [0] * 128
register = [0] * 8  # 8 register
SP = 7
pc = 0 # Program Counter, points to currently-executing instruction
    
running = True    
    
if len(sys.argv) != 2:
    print(f"Error: Proper Usage = {sys.argv[0]} filename")
    sys.exit(1)
try:
    with open(sys.argv[1]) as f:
        address = 0
      
        for line in f:
            num = line.split("#", 1)[0]
            
            if num.strip() == '':  # ignore comment-only lines
                continue
            # print(int(num))
            memory[address] = int(num)
            address += 1
        
except FileNotFoundError:
    print(f"{sys.argv[0]}: {sys.argv[1]} not found")
    sys.exit(2)
    
register[SP] = 127
while (running):
    command = memory[pc]
    if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1
        
    elif command == PRINT_NUM:
        operand = memory[pc + 1]
        print(operand)
        pc += 2
        
    elif command == SAVE_REGISTER:
        value = memory[pc + 1]
        regnum = memory[pc + 2]
        register[regnum] = value
        pc += 3
        
    elif command == PRINT_REGISTER:
        regnum = memory[pc + 1]
        print(register[regnum])
        pc += 2 
        
    elif command == PUSH:
        register[SP] -= 1               # Decrement the stack pointer
        regnum = memory[pc + 1]         # Get the register number operand
        value = register[regnum]        # Get the value from that register
        memory[register[SP]] = value    # Store that value in memory at the SP
        pc += 2
        
    elif command == POP:
        value = memory[register[SP]]    # Get value from memory at AT
        regnum = memory[pc + 1]         # Get the register number operand
        register[regnum] = value        # Store the value from the stack in the register
        register[SP] += 1               # Increment the stack pointer
        pc += 2

    elif command == CALL:
        #get address of instruction right after the CALL inst
        return_addr = pc + 2

        #push return address on stack
        register[SP] -= 1   #decrement the stack pointer
        memory[register[SP]] = return_addr  #store that value in memory at the SP
        
        # set the PC to the subroutine addr
        regnum = memory[pc+ 1]
        subroutine_addr = register[regnum]
        pc = subroutine_addr

    elif command == RET:
        # pop the return address off the stack
        return_addr = memory[register[SP]]
        register[SP] += 1

        pc =return_addr
    


    elif command == HALT:
        running = False
        pc += 1     
        
    else: 
        print(f"unknown instruction {command}")
        sys.exit(1)
    
    pc += 1