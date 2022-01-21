import numpy as np

class Dice:
    """ roll dice"""
    
    def __init__(self,amount,side):
        self.amount=amount
        self.side=side
        
    def r(self):
        """roll"""
        return np.sum(np.random.randint(1,self.side+1,self.amount))

class D20(Dice):
    
    def __init__(self):
        Dice.__init__(self,1,20)