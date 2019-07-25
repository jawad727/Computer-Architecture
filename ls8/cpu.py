 # Place where instructions are processed
"""CPU functionality."""
import sys
LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.SP = 7
        
    def __str__(self):
        return f"RAM: {self.ram}, REGISTER: {self.reg}, PC: {self.pc}"
    
    # MAR = address; _Memory Address Register_
    def ram_read(self, address):
        return self.ram[address]
    
    # MDR = value; _Memory Data Register_
    def ram_write(self, value, address):
        self.ram[address] = value
    def load(self):
        """Load a program into memory."""
        # program = [0] * 256
        if len(sys.argv) != 2:
            print(f"Error: Proper Usage = {sys.argv[0]} filename")
            sys.exit(1)
         
        try:
            with open(sys.argv[1]) as program:
                address = 0
                
                for line in program:
                    num = line.split("#", 1)[0]
                    
                    if num.strip() == '':  # ignores comment-only lines
                        continue
                    self.ram[address] = int(num, 2)
                    #print(num)
                    address += 1
           # print(self.ram)
                    
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.reg[i], end='')
    def run(self):
        """Run the CPU."""
        # determines whether or not this function is "running"
        running = True
        self.reg[self.SP] = 244
        # IR = _Instruction Register_
        
        
        while (running):
            IR = self.ram_read(self.pc)
            
            command = self.ram[self.pc]
            
            num_of_ops = int((IR >> 6) & 0b11) + 1
            
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
                
            # LDI = 0b10000010
            if command == LDI:
                # print('LDI', num_of_ops)
                self.reg[operand_a] = operand_b
            
            # PRN = 0b01000111
            elif command == PRN:
                # print('PRN', num_of_ops)    
                print(self.reg[operand_a])
               
            # HLT = 0b00000001
            elif command == HLT: 
                # print('HLT', num_of_ops)
                running = False

            elif command == MUL:
                # print("MUL")
                self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]

            elif command == PUSH:
                self.reg[self.SP] -= 1
                regnum = self.ram[self.pc + 1]
                value = self.reg[regnum]
                self.ram[self.reg[self.SP]] = value

            elif command == POP:
                value = self.ram[self.reg[self.SP]]
                regnum = self.ram[self.pc + 1]
                self.reg[regnum] = value
                self.reg[self.SP] += 1

            else: 
                print(f"unknown instruction: {command}")
                sys.exit(1)
            
            self.pc += num_of_ops