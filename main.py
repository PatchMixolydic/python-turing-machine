"""
Turing machine in Python
Recommended alphabet: "_", "0", "1"
"""

LEFT = -1
RIGHT = 1
VERBOSE = False

# 2-state busy beaver. Intended result: 1 1 1 1
bb2 = {
    "A": {
        "_": ["1", RIGHT, "B"],
        "0": ["1", RIGHT, "B"],
        "1": ["1", LEFT, "B"]
    },
    "B": {
        "_": ["1", LEFT, "A"],
        "0": ["1", LEFT, "A"],
        "1": ["1", RIGHT, "HALT"]
    }
}

# 3-state busy beaver. Intended result: 1 1 1 1 1 1
bb3 = {
    "A": {
        "_": ["1", RIGHT, "B"],
        "0": ["1", RIGHT, "B"],
        "1": ["1", RIGHT, "HALT"]
    },
    "B": {
        "_": ["0", RIGHT, "C"],
        "0": ["0", RIGHT, "C"],
        "1": ["1", RIGHT, "B"]
    },
    "C": {
        "_": ["1", LEFT, "C"],
        "0": ["1", LEFT, "C"],
        "1": ["1", LEFT, "A"]
    }
}

# NOT program. Intended result: NOT(tape)
notProg = {
    "main": {
        "_": ["_", RIGHT, "HALT"],
        "0": ["1", RIGHT, "main"],
        "1": ["0", RIGHT, "main"]
    }
}

# AND two 8bit numbers. Input: (8bit binary number) _ (8bit binary number), Intended result: _ _ _ _ _ _ _ _ _ AND(tape1 _ tape2)
and8bit = {
    "main": { # Reading the first digit
        "_": ["_", LEFT * 8, "clearTape"], # Hit number terminator, clear the first number
        "0": ["0", RIGHT * 9, "and0"], # We have a zero, go forward to the second 8 bit number
        "1": ["1", RIGHT * 9, "and1"] # One, go forward to second 8 bit number
    },
    "and0": {
        "_": ["ERROR0", LEFT, "HALT"], # Uh oh! We can't and a 0 and _
        "0": ["0", LEFT * 8, "main"], # 0 AND 0 = 0, go to the next digit in the first number
        "1": ["0", LEFT * 8, "main"]
    },
    "and1": {
        "_": ["ERROR1", LEFT, "HALT"], # Oh no!
        "0": ["0", LEFT * 8, "main"],
        "1": ["1", LEFT * 8, "main"]
    },
    "clearTape": {
        "_": ["_", RIGHT, "HALT"], # end of the first number, it's all gone now
        "0": ["_", RIGHT, "clearTape"],
        "1": ["_", RIGHT, "clearTape"]
    }
}

class TuringMachine:
    def __init__(self, program):
        self.tape = {}
        self.program = program
        self.currentIdx = 0
        self.currentState = list(self.program.keys())[0]
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.step()

    def loadTape(self, contents):
        for i in range(len(contents)):
            letter = contents[i]
            self.tape[i] = letter

    def readTape(self):
        result = self.tape.get(self.currentIdx)
        if result == None:
            result = "_"
            self.tape[self.currentIdx] = "_"
        return result

    def step(self):
        if self.currentState == "HALT":
            self.halt()
            return
        stateInstructions = self.program.get(self.currentState)
        if stateInstructions == None:
                raise RuntimeError("Invalid state {0}".format(self.currentState))
        result = self.readTape()
        instructions = stateInstructions.get(result)
        if instructions == None:
            print("Warning -- Instruction not found for state {0} character {1} at index {2}. Halting...".format(self.currentState, result, self.currentIdx))
            self.halt()
            return
        self.tape[self.currentIdx] = instructions[0]
        self.currentIdx += instructions[1]
        self.currentState = instructions[2]
        if VERBOSE:
            print("STATE: {0}".format(self.currentState))
            print("IDX: {0}".format(self.currentIdx))
            print("TAPE:", end = " ")
            for _, val in self.tape.items():
                print(val, end = " ")
            print("\n")

    def halt(self):
        self.running = False
        print("Halted.")
        print("TAPE:", end = " ")
        for _, val in self.tape.items():
            print(val, end = " ")
        print("\n")

amachine = TuringMachine(and8bit)
amachine.loadTape("11010100_11011000")
amachine.run()
