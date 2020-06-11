import sys
import Default

INF = sys.maxsize
ALPHA = 1.1
BETA = 0.1
    

class ObjectiveVal(object):
    def __init__(self, bd = INF, al = 1):
        self.bd = bd
        self.al = al

    def best_answer(self):
        return self.bd == 0 and self.al == 0

    def omega(self, ty):
        if ty == 0:
            return 1.0 - ALPHA**(-self.al)
        if ty == 1:
            return self.al / (self.al + BETA)

    def normalize(self):
        return self.omega(Default.NORMALIZATION_DEF)    

    def better_than(self, other):
        if (self.bd < other.bd):
            return True
        if (self.bd > other.bd):
            return False
        if (self.al < other.al):
            return True
        return False