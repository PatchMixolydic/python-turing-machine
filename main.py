"""
Turing machine in Python
Recommended alphabet: "_", "0", "1"
Spaces are disallowed in alphabets when pre-loading tapes; they are used as optional delimiters. Use "_" instead.
"""
import json, collections

VERBOSE = False

class TuringMachine:
    def __init__(self, program):
        self.tape = collections.OrderedDict()
        for i in range(-5, 5):
            self.tape[i] = "_"
        self.program = program
        self.currentIdx = 0
        self.currentState = self.program.get("initState", "init")
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.step()

    def loadTape(self, contents):
        contents = contents.replace(" ", "")
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

if __name__ == '__main__':
    filename = input("What program would you like to run? (include extension): ")
    with open(filename) as programFile:
        program = json.load(programFile)
    initTape = input("Initial value for tape (blank for none): ")

    amachine = TuringMachine(program)
    if initTape: amachine.loadTape(initTape)
    amachine.run()
