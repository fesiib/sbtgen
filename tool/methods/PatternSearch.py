import worker.Evaluator as Evaluator
import data.ObjectiveVal as ObjectiveVal

class PatternSearch:
    def __init__(self, acc_factor):
        self.acc_factor = acc_factor
    
    def evaluate(self):
        return Evaluator.evaluate(self.vector, self.str_branch, self.path_branch)

    def initialize(self):
        self.initial = self.evaluate()
        self.dir = 0
        self.modifier = 1
    

    def setup(self, vector, pos, branch, path_branch):
        self.pos = pos
        self.vector = vector
        self.str_branch = branch
        self.path_branch = path_branch
        self.num = vector[pos]
        self.initialize()

    def explore(self):
        self.vector[self.pos] -= self.modifier
        lef = self.evaluate()
        self.vector[self.pos] += 2 * self.modifier
        rig = self.evaluate()

        self.vector[self.pos] = self.num

        self.last = self.initial
        if lef.better_than(self.initial):
            self.dir = -1
            self.next = lef
        elif rig.better_than(self.initial):
            self.dir = 1
            self.next = rig
        else:
            self.dir = 0
            self.next = self.initial
        
        self.num += self.dir * self.modifier
        self.vector[self.pos] = self.num
        return self.dir != 0


    def pattern_move(self):
        while (self.next.better_than(self.last)):
            self.last = self.next
            
            self.modifier *= self.acc_factor
            self.num += self.modifier * self.dir
            self.vector[self.pos] = self.num

            self.next = self.evaluate()
            if (self.next.better_than(self.last) == False):
                self.num -= self.modifier * self.dir
                self.vector[self.pos] = self.num