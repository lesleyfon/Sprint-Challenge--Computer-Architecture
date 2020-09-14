"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8
        self.ram = [None] * 256
        self.pc = 0  # Program Counter, address of the currently executing instruction

        self.memory_loc = 0
        self.SP = 7
        self.is_on = True
        self.FL = {
            "E": None,
            "L": None,
            "G": None
        }
        self.instructions = {
            "LDI": 0b10000010,  # Set the value of a register to an integer.
            # Print numeric value stored in the given register.
            "PRN": 0b01000111,
            'HLT': 0b00000001,

            # MUL R0,R1 Multiply the values in two registers together and store the result in registerA.
            "MUL": 0b10100010,

            "PUSH": 0b01000101,

            # PUSH register

            # Push the value in the given register on the stack.

            # Decrement the SP.
            # Copy the value in the given register to the address pointed to by SP.

            "POP": 0b01000110,

            "CALL": 0b01010000,
            "RET": 0b00010001,
            "ADD": 0b10100000,
            "CMP": 0b10100111,
            "JMP": 0b01010100,
            "JEQ": 0b01010101,
            "JNE": 0b01010110

        }

    def load(self):
        """Load a program into memory."""

        file_name = sys.argv
        if len(file_name) == 1:
            print("Provide a file name ro read instructions from")
            sys.exit(1)
        address = 0
        with open(f"/Users/lesley/code/Python/Projects/Computer-Architecture/ls8/examples/{file_name[1]}") as f:
            for line in f:
                line = line.split("#")
                line = line[0]
                line = line.strip()

                if line == "":
                    continue
                else:
                    num = int(line, 2)
                    self.ram[address] = num
                    address += 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        '''
            Value = Args1 \n
            Address = Args2
        '''

        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    a = ["00011000", "00011000", ]

    def run(self):
        self.register[self.SP] = 244
        self.pc = 0
        """
            Run the CPU.

        """

        while self.is_on:

            instruction = self.ram[self.pc]

            if instruction == self.instructions["LDI"]:

                num = self.ram[self.pc + 2]
                reg_loc = self.ram[self.pc + 1]

                self.register[reg_loc] = num

                self.pc += 3

            elif instruction == self.instructions["PRN"]:

                print(self.register[self.ram[self.pc + 1]])

                self.pc += 2

            elif instruction == self.instructions["MUL"]:
                # convert R1 and R1 to Interger Numbers
                R1 = self.ram[self.pc + 1]
                R2 = self.ram[self.pc + 2]

                product = self.register[R1] * self.register[R2]
                self.register[R1] = product
                self.pc += 3
            elif instruction == self.instructions["ADD"]:
                # convert R1 and R1 to Interger Numbers
                R1 = self.ram[self.pc + 1]
                R2 = self.ram[self.pc + 2]

                product = self.register[R1] + self.register[R2]
                self.register[R1] = product
                self.pc += 3

            elif instruction == self.instructions["HLT"]:
                self.is_on = False
                self.pc += 1

            elif instruction == self.instructions["PUSH"]:
                self.register[self.SP] -= 1

                reg_index = self.ram[self.pc + 1]

                reg_val = self.register[reg_index]

                self.ram[self.register[self.SP]] = reg_val

                self.pc += 2

            elif instruction == self.instructions["POP"]:

                given_reg = self.ram[self.pc + 1]
                # Write the value in memory at the top of stack to the given register
                value_from_ram = self.ram[self.register[self.SP]]

                self.register[given_reg] = value_from_ram
                # increment the stack pointer
                self.register[self.SP] += 1
                self.pc += 2
            elif instruction == self.instructions['CALL']:
                # gett the given register in the operand

                given_reg = self.ram[self.pc + 1]

                self.register[self.SP] -= 1
                self.ram[self.register[self.SP]] = self.pc + 2

                self.pc = self.register[given_reg]

            elif instruction == self.instructions['RET']:
                self.pc = self.ram[self.register[self.SP]]
                self.register[self.SP] += 1

            elif instruction == self.instructions['CMP']:
                '''
                This is an instruction handled by the ALU.
                CMP registerA registerB

                Compare the values in two registers.

                If they are equal, set the Equal E flag to 1, otherwise set it to 0.

                If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.

                If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.


                '''
                R1 = self.ram[self.pc + 1]
                R2 = self.ram[self.pc + 2]

                reg1_val = self.register[R1]
                reg2_val = self.register[R2]

                if reg1_val == reg2_val:
                    self.FL["E"] = 1

                else:
                    self.FL["E"] = 0

                if reg1_val < reg2_val:
                    self.FL["L"] = 1
                else:
                    self.FL["L"] = 0

                if reg1_val > reg2_val:
                    self.FL["G"] = 1

                else:
                    self.FL["G"] = 0

                self.pc += 3

            elif instruction == self.instructions['JMP']:

                '''
                    JMP
                    JMP register

                    Jump to the address stored in the given register.

                    Set the PC to the address stored in the given register.

                    Machine code:
                '''

                reg_address = self.ram[self.pc + 1]

                self.pc = self.register[reg_address]

            elif instruction == self.instructions['JEQ']:
                '''
                JEQ register

                If equal flag is set (true), jump to the address stored in the given register.
                '''

                if self.FL["E"] == 1:
                    reg_address = self.ram[self.pc + 1]
                    self.pc = self.register[reg_address]

                else:
                    self.pc += 2

            elif instruction == self.instructions['JNE']:
                '''
                    JNE
                    JNE register

                    If E flag is clear (false, 0), jump to the address stored in the given register.
                '''
                if self.FL["E"] == 0:

                    reg_address = self.ram[self.pc + 1]
                    self.pc = self.register[reg_address]

                else:
                    self.pc += 2
                pass
            elif instruction not in self.instructions:

                print(f"Unknown instruction {instruction}")
                sys.exit(1)
            else:
                self.pc += 1
                if self.pc == len(self.ram):
                    self.is_on = False
