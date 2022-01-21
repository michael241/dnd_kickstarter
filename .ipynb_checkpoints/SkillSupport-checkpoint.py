import numpy as np
    
class SkillConvert:
    """converts raw attribute/score into its modifider"""
    
    def __init__(self):
        """initalizer"""
        pass
    
    def mod(self,score):
        if score <= 1:
            return -5
        elif score in [2,3]:
            return -4
        elif score in [4,5]:
            return -3
        elif score in [6,7]:
            return -2
        elif score in [8,9]:
            return -1
        elif score in [10,11]:
            return 0
        elif score in [12,13]:
            return 1
        elif score in [14,15]:
            return 2
        elif score in [16,17]:
            return 3
        elif score in [18,19]:
            return 4
        elif score in [20,21]:
            return 5
        elif score in [22,23]:
            return 6
        elif score in [24,25]:
            return 7
        elif score in [26,27]:
            return 8
        elif score in [28,29]:
            return 9
        elif score in [30,31]:
            return 10
        elif score in [32,33]:
            return 11
        elif score in [34,35]:
            return 12
        else:
            return 13
        
class ProficiencyBonusConvert:
    """converts level into proficinecy bonus for classes"""
    
    def mod(self,score):
        if score in [1,2,3,4]:
            return 2
        elif score in [5,6,7,8]:
            return 3
        elif score in [9,10,11,12]:
            return 4
        elif score in [13,14,15,16]:
            return 5
        elif score in [17,18,19,20]:
            return 6
        elif score in [21,22,23,24]:
            return 7
        else:
            return 8
        
class MovementConversion:
    """ converts feet into squares that are able to be moved"""
    def con(self,feet,zero_threshold=2.5):
        
        #tiny movements cannot move
        if feet <= zero_threshold:
            return 0
        
        #above tiny movements, some movement allowed
        #integer and must fully get into next square to make the move
        else:
            return int(np.floor((feet+2.5)/5))
        