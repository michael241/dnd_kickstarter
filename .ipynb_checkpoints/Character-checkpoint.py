import numpy as np
from Dice import * 
from SkillSupport import *
import matplotlib.pyplot as plt

#https://jckantor.github.io/ND-Pyomo-Cookbook/
import pyomo.environ as pe
    
class Character:
    """ baseline character class, underpinning all PCS and NPC
    
    """
    def __init__(self
                 ,name=None
                 ,icon=None
                 ,level= None
                 ,team=None
                 ,hit_point_current=None
                 ,hit_point_max = None
                 ,hit_dice = None
                 ,general_status='alive_and_well' #options, alive_and_well or deceased
                 ,advantage_status='base'
                 ,initative = None
                 ,x = None
                 ,y = None
                 ,x_target = None
                 ,y_target = None
                 ,armor=None
                 ,speed=None
                 ,sth=None
                 ,dex=None
                 ,con=None
                 ,inl=None
                 ,wis=None
                 ,cha=None
                 ,proficiency_bonus=None
                 ,proficiency_list=[]
                 ,expertise_list=[]
                 ,enemy_list=[]
                ):
        "initalizer"
        
        #general
        self.name = name
        self.icon = icon
        self.level = level
        self.hit_point_current = hit_point_current
        self.hit_point_max = hit_point_max
        self.hit_dice = hit_dice
        self.armor = armor
        self.speed = speed
        self.general_status = general_status
        self.advantage_status = advantage_status
        self.initative = initative
        
        #movemement
        self.x = x
        self.y = y
        self.x_target = x_target
        self.y_target = y_target
        
        #base abilities
        self.sth = sth
        self.dex = dex
        self.con = con
        self.inl = inl
        self.wis = wis
        self.cha = cha
        
        #battle
        self.team= team
        self.enemy_list = enemy_list
        
        #misc
        self.proficiency_bonus = proficiency_bonus
        self.proficiency_list = proficiency_list
        self.expertise_list= expertise_list
        
    def CheckMod(self,check):
        """returns basic mod for core ability or skill check"""

        #get base value add
        if check in ['stn','athletics']:
            mod = self.sth
            
        elif check in ['dex','acrobatics','sleight_of_hand','stealth']:
            mod = self.dex
            
        elif check in ['con']:
            mod = self.con
        
        elif check in ['inl','arcana','history','investigation','nature','religion']:
            mod = self.inl
        
        elif check in ['wis','animal_handling','insight','medicine','perception','survival']:
            mod = self.wis
            
        elif check in ['cha','deception','intimidation','performance','persuasion']:
            mod = self.cha
            
        else:
            raise ValueError("Character BaseCheck - check read in that is neither attribute or skill")
        
        #convert to modifer
        mod = SkillConvert().mod(mod)
        
        #handle proficiney bonuses where applicable
        if check in self.proficiency_list:
            proficiency_bonus = self.proficiency_bonus
            
        #handle experise bonous
        elif check in self.expertise_list:
            proficiency_bonus = self.proficiency_bonus*2
            
        #otherwise no bonus added
        else:
            proficiency_bonus = 0
            
        #handle expertise bones 
            
        #return (done in two steps in case we want to make custom changes later
        return mod + proficiency_bonus
    
    
    def CheckModBase(self,check):
        """surface the baseline modifier of the skill or ability"""
        return self.CheckMod(check)
    
    def Check(self,check):
        """ability and skill check"""
        
        #base role
        if self.advantage_status == 'base':
            return D20().r()+self.CheckModBase(check)
        
        #top of two roles if has advantage
        elif self.advantage_status  == 'advantage':
            return np.max([D20().r()+self.CheckModBase(check),
                           D20().r()+self.CheckModBase(check)])
        
        #bottom of two roles if no advantage
        elif self.advantage_status  == 'disadvantage':
            return np.min([D20().r()+self.CheckModBase(check),
                           D20().r()+self.CheckModBase(check)])
        
        #else trigger exception
        else:
            raise ValueError("Character Check - advantage inputted that is not in approved list")
            
    def Plot(self):
        #show icon
        plt.annotate(self.icon,
                     xy=(self.x,self.y),
                     fontsize=50,
                     horizontalalignment='center',
                     verticalalignment='center')
            
        #show hp
        plt.annotate(self.hit_point_current,
                     xy=(self.x,self.y+0.3),
                     fontsize=25,
                     horizontalalignment="center",
                     verticalalignment="center")
            
            
    def Setup(self):
        """for essential values ensure they are calculated, or otherwise flag error"""
        #set baseline hitpoints
        if self.hit_point_max == None:
           self.hit_point_max = np.max([-1,self.hit_dice.r()*self.level + self.CheckMod('con')])
        
        #set current hit points (to max)
        if self.hit_point_current == None:
            self.hit_point_current = self.hit_point_max 
           
        #set baseline proficiency bonus
        if self.proficiency_bonus == None:
            self.proficiency_bonus = ProficiencyBonusConvert().mod(self.level)

            
    def AttackMelee(self):
        """melee attack placeholder"""
        
        
        
        
        
        
