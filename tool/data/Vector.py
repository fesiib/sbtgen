from random import Random
import sys

class Vector():

    
    def __init__(self, leng = 0):
        self.mmin = -sys.maxsize
        self.mmax = sys.maxsize

        self.vars = []
        self.leng = leng
        self.initialize_with_zeros()
    
    
    def initialize_with_zeros(self):
        self.vars = []
        for i in range(self.leng):
            self.vars.append(0)
    
    def initialize_with_rd(self):
        self.vars = []
        for i in range(self.leng):
            self.vars.append(Random().randint(a = self.mmin + 1, b = self.mmax - 1))
    
    def initialize_with_rd_small(self):
        self.vars = []
        for i in range(self.leng):
            self.vars.append(Random().randint(a = -100, b = 100))
    def initialize_with_rd_medium(self):
        self.vars = []
        for i in range(self.leng):
            self.vars.append(Random().randint(a = -1000000, b = 1000000))
    