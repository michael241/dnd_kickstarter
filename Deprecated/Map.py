import numpy as np
import math
from scipy.spatial.distance import cityblock
from Character import *
from SkillSupport import * 


class Map:
    """ field of action where characters interact"""
    
    def __init__(self,
                 name,
                 x_min = 0,
                 x_max = 10,
                 y_min = 0,
                 y_max = 10,
                 square_size = 5,
                 map_character = None,
                 map_elevation = None,
                 map_difficulty = None):
        """initalizer"""
        
        #general
        self.name = name
        
        #dimensions
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        
        #list of active characters and static objects
        self.list_character = []
        self.list_static = []
        self.square_size = square_size
        
        #make the map (note use np.rot90 so x and y coordinates make sense)
        if map_character == None:
            self.map_character = np.full((1+y_max - y_min,1+x_max - x_min), " ", dtype=str)
            
        if map_elevation == None:
            self.map_elevation = np.ones((1+y_max - y_min,1+x_max - x_min), dtype = int) 
        
        if map_difficulty == None:
            self.map_difficulty = np.full((1+y_max - y_min,1+x_max - x_min), square_size, dtype = int)
        
    def CharacterErasePlot(self,Character):
        """ erase character so they can be moved"""
        
        #only proceed if Chracter in plot
        if Character.icon not in np.unique(self.map_character):
            raise Exception("Error: Character " + Character.name + " attempt toerase but not already mapped")
            
        #erase character
        #note the character is still in the characters we care about
        self.map_character[self.map_character==Character.icon] = ' '
    
    def CharacterPlot(self,Character):
        """ plot character onto map"""
        
        #plot in new spot
        self.map_character[Character.x_pos][Character.y_pos] = Character.icon
        
        
    def CharacterAdd(self,Character):
        """add a character to the map"""
        
        #raise error if character already in list 
        if Character.name in [x.name for x in self.list_character]:
            raise Exception("Error: Character " + Character.name + " already mapped")
        
        #otheriwse add to list of known characters
        self.list_character += [Character]
        
        #and plot initial
        self.CharacterPlot(Character)
        
    def StaticAdd(self,x_pos,y_pos):
        """add static object to the map, cannot be moved"""
        
        #note as static
        self.list_static += [Character(name='wall',x_pos=x_pos,y_pos=y_pos)]
        
        #add into plot
        self.map_character[x_pos][y_pos] = "█"
        
        
    def CharacterProceedToGround(self,Character,x_pos,y_pos):
        """movement, incrementally calculated 
        note, character will proceed one step at a time and deal with difficulty
        """
        
        ####
        #### validateion checks 
        ####
        
        #validate character mapped
        if Character.name not in [x.name for x in self.list_character]:
            raise Exception("Error: Character " + Character.name + " not known")
        
        #validate character already on map
        if Character.icon not in np.unique(self.map_character):
            raise Exception("Error: Character " + Character.name + " known but not on map")
        
        ####
        #### retrieve basic information and parameters
        ####
        
        #get current location (prime while loop)
        x_pos_current = Character.x_pos
        y_pos_current = Character.y_pos
        
        #list occupied spots (except for this character
        list_occupy = ([(x.x_pos,x.y_pos) for x in self.list_character] + [(x.x_pos,x.y_pos) for x in self.list_static])
        list_occupy.remove((Character.x_pos,Character.y_pos))
        
        #note movement budget
        movememt_budget = Character.speed
        
        ####
        #### proceed one step at a time until reach distination or out of movembers
        ####
        while movememt_budget > 0:
            
            #break if we have reached our destination
            if ((x_pos == x_pos_current) & (y_pos == y_pos_current)):
                break
            
            #hold eligible steps and hold distance
            list_eligible = []
            list_blocker = []
            
            #iterate through x an y combination
            for x_look in [x_pos_current-1,x_pos_current,x_pos_current+1]:
                for y_look in [y_pos_current-1,y_pos_current,y_pos_current+1]:
                    
                    #note cells that are blockers
                    if (x_look,y_look) in [(x.x_pos,x.y_pos) for x in self.list_static]:
                        list_blocker +=  [(x_look,y_look,[x.avoid for x in self.list_static if x.x_pos == x_look and x.y_pos == y_look])]
 
                    #options for next steps    
                    #check if cell is not occupied
                    if (x_look,y_look) not in list_occupy:
                            
                        #check if cell is in bounds
                        if ((self.x_min <= x_look <= self.x_max) & (self.y_min <= y_look <= self.y_max)):
                            #check if we can move into the cell with suffient movement
                            #no cost for current location 
                            if (movememt_budget >= self.map_difficulty[x_look][y_look]) | ((x_look==x_pos_current)&(y_look==y_pos_current)):
                                
                                #if all the conditions are true, then include in eligible list
                                list_eligible += [(x_look,y_look)]
             
            #if no eligible steps (only can stay put), stay put
            if len(list_eligible) == 1 :
                
                #put budget to zero - we are stuck
                break
            
            ###
            ### handle walls
            ###
            print(list_blocker)
            if len(list_blocker) >=  1:
                
                # determine relative position
                wall_overall_x = np.mean([x for x,_,_ in list_blocker])
                wall_overall_y = np.mean([y for _,y,_ in list_blocker])
                print(wall_overall_x,x_pos_current,wall_overall_y,y_pos_current)
                
                         
                # if in 12 oclock position,
                if (wall_overall_x<=x_pos_current)&(wall_overall_y<=y_pos_current):
                    print("12-3")
                    
                    #subset to top row, maximize y
                    list_eligible = [(x,y) for x,y in list_eligible if y == min([y for x,y in list_eligible])]
                    
                    #if multiple options maximize x
                    if len(list_eligible) > 1:
                        
                        #subset
                        list_eligible = [(x,y) for x,y in list_eligible if x == min([x for x,y in list_eligible])]
                        
                #if in 9 oclock position, with structure center of the clock
                elif (wall_overall_x>=x_pos_current)&(wall_overall_y<=y_pos_current):
                    print("9-12")
                    
                    #subset to top row, maximize y
                    list_eligible = [(x,y) for x,y in list_eligible if x == max([x for x,y in list_eligible])]
                    
                    #if multiple options maximize x
                    if len(list_eligible) > 1:
                        
                        #subset
                        list_eligible = [(x,y) for x,y in list_eligible if y == max([y for x,y in list_eligible])]
                
                #if in 3 oclock position
                elif  (wall_overall_x<=x_pos_current)&(wall_overall_y>=y_pos_current):
                    print('3-6')
                    
                    #subset to top row, maximize y
                    list_eligible = [(x,y) for x,y in list_eligible if x == min([x for x,y in list_eligible])]
                    
                    #if multiple options maximize x
                    if len(list_eligible) > 1:
                        
                        #subset
                        list_eligible = [(x,y) for x,y in list_eligible if y == max([y for x,y in list_eligible])]
                
                #if in 6 oclock position (else)
                elif ((wall_overall_x >= x_pos_current) & (wall_overall_y >= y_pos_current)):
                    print('6-9')
                    
                    #subset to top row, maximize y
                    list_eligible = [(x,y) for x,y in list_eligible if y == max([y for x,y in list_eligible])]
                    
                    #if multiple options maximize x
                    if len(list_eligible) > 1:
                        
                        #subset
                        list_eligible = [(x,y) for x,y in list_eligible if x == max([x for x,y in list_eligible])]
                    
                else:
                    print('Error')
                
                
                
            
            ###
            ### handle wider open areas
            ###
            
            else:
                #if we can move, proceed to find optimal next step
                #for each eligible cell determine distance to destination, mahattan
                list_distance = np.array([cityblock([x,y],[x_pos,y_pos]) for x,y in list_eligible])
            
                #reduce eligible list to those with the smallest distances
                list_eligible = np.array(list_eligible)[list_distance==min(list_distance)]
                
                #sort and order
                list_eligible = [x for _, x in sorted(zip(list_distance, list_eligible))]
            
            ###
            ###update position
            ###
            x_pos_current,y_pos_current  = list_eligible[0]
            
            #reduce budget for moving to new squares
            movememt_budget = movememt_budget-self.map_difficulty[x_pos_current][x_pos_current]
            
        #move to final new position
        #set characters new x_pos and y_pos (limited based on speed)
        Character.x_pos, Character.y_pos = x_pos_current,y_pos_current 
        
        #erase on map
        self.CharacterErasePlot(Character)
        
        #move to new location
        self.CharacterPlot(Character)
            
                            

            
            
        
            
    def CharacterProceedToFlight(self,Character,x_pos,y_pos):
        """have character proceed to a new space in flight
        note while these characters cannot stop in walls, they can proceed over or in them
        character does not dael with difficulty"""
        
        ####
        #### validateion checks 
        ####
        
        #validate character mapped
        if Character.name not in [x.name for x in self.list_character]:
            raise Exception("Error: Character " + Character.name + " not known")
        
        #validate character already on map
        if Character.icon not in np.unique(self.map_character):
            raise Exception("Error: Character " + Character.name + " known but not on map")
        
        ####
        #### retrieve basic information and parameters
        ####
        #once character is known and mapped, record and move them
        x_pos_original,y_pos_original = Character.x_pos, Character.y_pos
        
        #list occupied spots (except for this character
        list_occupy = ([(x.x_pos,x.y_pos) for x in self.list_character] + [(x.x_pos,x.y_pos) for x in self.list_static])
        list_occupy.remove((Character.x_pos,Character.y_pos))

        #note that we can preocced and re proceed until perfect
        looper = True
        
        ####
        #### initiate loop for validating movement
        ####
        
        while looper == True:

            ####
            #### handle cases where distance is too far for character to manuever to
            ####

            #calculate distance
            #adjust to the center of the square (cv = center value)

            distance = ((x_pos_original-x_pos)**2+(y_pos_original-y_pos)**2)**0.5 *self.square_size 

            #no action if speed accounts for that movement
            #ie only subset the distance if character cannot move that far
            if distance > Character.speed: 

                #shorten distance down to the distance that we have available to us
                #distance can also be through of as radius
                #adding the 2.5 square feet from where they currenly are
                distance = Character.speed 

                #determine the angle
                angle = math.atan2((x_pos-x_pos_original),(y_pos-y_pos_original))

                #determine the side
                #movememet conversion will arrive back at teh coordiantes of interest
                side_x = MovementConversion().con(distance * math.sin(angle))
                side_y = MovementConversion().con(distance * math.cos(angle))

                #reset x and y
                x_pos, y_pos = x_pos_original + side_x,y_pos_original + side_y

            ####
            #### handle cases where the spot the character is going is obstructed
            ####
            
            #move to new destination if cannot get to point of interest
            #minimze distance
            while (x_pos,y_pos) in list_occupy:

                #randomly adjust up or down a square, one of the values
                #if this value is not in the obstruction list
                if np.random.randint(0,2) == 1:
                    x_pos,  y_pos = x_pos + np.random.choice([-1,1]),y_pos
                else:
                    x_pos,  y_pos = x_pos ,y_pos + np.random.choice([-1,1])
            ####
            #### validate that the location is a valid coordinate (not outside of the map)
            ####
            validSpot = True
            
            #bump up minmums if needed
            if x_pos < self.x_min:
                x_pos = self.x_min
                validSpot = False
                
            if y_pos < self.y_min:
                y_pos = self.y_min
                validSpot = False
                
            if x_pos > self.x_max:
                x_pos = self.x_max
                validSpot = False
                
            if y_pos > self.y_max:
                y_pos = self.y_max
                validSpot=False
            
            #validate if within distance and open square and inbounds - then exit
            if (x_pos,y_pos) not in list_occupy and distance <= Character.speed and validSpot==True:
                looper = False
                
        #if character able to proceed to space, then place in position
        #set characters new x_pos and y_pos (limited based on speed)
        Character.x_pos, Character.y_pos = x_pos,y_pos
        
        #erase on map
        self.CharacterErasePlot(Character)
        
        #move to new location
        self.CharacterPlot(Character)
        
        
        
            
        
        
        
        