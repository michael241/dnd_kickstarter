import numpy as np

class Dice:
    """ roll dice"""
    
    def __init__(self,amount,side,adder=0):
        """
        
        Args:
            amount = number of dice simulated
            side = sides per dice (uniformally labeled 1- max)
            adder = flat addition done on outcome
        
        """
        
        self.amount=amount
        self.side=side
        self.adder=adder
        
    def r(self):
        """roll"""
        return np.sum(np.random.randint(1,self.side+1,self.amount))+self.adder

class D20(Dice):
    
    def __init__(self):
        Dice.__init__(self,1,20,0)