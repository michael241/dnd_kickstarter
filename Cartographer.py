from SquareGraph import * 

class Cartographer:
    """make maps, with commands rather than handwriting"""
    
    def _init_(self,map_holder=None,x_min=0,y_min=0,x_max=25,y_max=25):
        self.map_holder = map_holder
        self.x_min = 0
        self.y_min = 0
        self.x_max = 0
        self.y_max = 0
    
    def Background(self,x,y,b="OOO",l="w",d=5):
        """ make the background object that we can then edit """
        
        #set up new map
        new_map_holder = []
        
        #iterate through all x and y cominations to fill out complete grid
        for x_current in range(x):
            for y_current in range(y):
                
                #populate each square 
                new_map_holder += [Square(x_current,y_current,b=b,l=l,d=d)]
                
          
        #sort so order makes intutive sense
        new_map_holder.sort(key=lambda n:n.x+(n.y*(x-0)))
        
        #set map
        self.map_holder = new_map_holder
        self.x_min = 0
        self.y_min = 0
        self.x_max = x
        self.y_max = y
        
    def UpdateSquare(self,x,y,b,l):
        """for a specfic square in the list swap it out for this new one"""
        self.map_holder[x+(y*(self.x_max-self.x_min))].b = b
        self.map_holder[x+(y*(self.x_max-self.x_min))].l = l
        
    def UpdateArea(self,x_start,y_start,x_end,y_end,b="000",l="white",edge_maker=False):
        """update a specific area with new color and borders
        
        Attribute:
            x_start: lowest x
            y_start: lowest y 
            x_end: highest x (inclusive)
            y_end: highest y (inclusive)
        """
        
        #if no edge
        if edge_maker == False:
        
            #target list,overall
            xy = []
            for x_finder in np.arange(x_start,x_end+1,1):
                for y_finder in np.arange(y_start,y_end+1,1):
                    xy += [(x_finder,y_finder)]


            #iterate through and assign values for inside area
            for node in xy:
                self.UpdateSquare(x=node[0],y=node[1],b=b,l=l)
                
        #if edge
        if edge_maker == True:
            
            #check if linear corridor (one node wide)
            #long x, short y
            if y_start == y_end:
                
                #iterate through x
                for x_finder in np.arange(x_start,x_end+1,1):
                    
                    #build start endcap
                    if x_finder == x_start:
                        self.UpdateSquare(x=x_finder,y=y_start,b="OE",l=l)
                        
                    #build end end cap
                    elif x_finder == x_end:
                        self.UpdateSquare(x=x_finder,y=y_start,b="OW",l=l)
                        
                    #otherwise build the top and bottom of the corridor
                    else:
                        self.UpdateSquare(x=x_finder,y=y_start,b="PWE",l=l)
                        
            #check if linear corridor (one node wide)
            #long y, short x
            elif x_start == x_end:
                
                #iterate through x
                for y_finder in np.arange(y_start,y_end+1,1):
                    
                    #build start endcap
                    if y_finder == y_start:
                        self.UpdateSquare(x=x_start,y=y_finder,b="ON",l=l)
                        
                    #build end end cap
                    elif y_finder == y_end:
                        self.UpdateSquare(x=x_start,y=y_finder,b="OS",l=l)
                        
                    #otherwise build the top and bottom of the corridor
                    else:
                        self.UpdateSquare(x=x_start,y=y_finder,b="PNS",l=l)
                        
            #otherwise it is a rectangle and we can iterate through
            else:
                
                #iterate through all x and y
                for x_finder in np.arange(x_start,x_end+1,1):
                    for y_finder in np.arange(y_start,y_end+1,1):
                        
                        #corner NW
                        if x_finder == x_start and y_finder == y_end:
                            self.UpdateSquare(x=x_finder,y=y_finder,b="CNW",l=l)
                        
                        #corner NE
                        elif x_finder == x_end and y_finder == y_end:
                            self.UpdateSquare(x=x_finder,y=y_finder,b="CNE",l=l)
                        
                        #corner SE
                        elif x_finder == x_end and y_finder == y_start:
                            self.UpdateSquare(x=x_finder,y=y_finder,b="CSE",l=l)
                            
                        #corner SW
                        elif x_finder == x_start and y_finder == y_start:
                            self.UpdateSquare(x=x_finder,y=y_finder,b="CSW",l=l)  
                            
                        #side north
                        elif y_finder == y_end:
                            self.UpdateSquare(x=x_finder,y=y_finder,b="BN",l=l)
                        
                        #side east
                        elif x_finder == x_end:
                            self.UpdateSquare(x=x_finder,y=y_finder,b="BE",l=l)
                            
                        #side south
                        elif y_finder == y_start:
                            self.UpdateSquare(x=x_finder,y=y_finder,b="BS",l=l)
                        
                        #side west
                        elif x_finder == x_start:
                            self.UpdateSquare(x=x_finder,y=y_finder,b="BW",l=l)
                            
                        #else, the space that was given
                        else:
                            self.UpdateSquare(x=x_finder,y=y_finder,b=b,l=l)
                            
    def Show(self):
        """in the proper grid format, show the network"""
        
        #work way from top left to bottom right
        print("[")
        for y in np.arange(self.y_max-1,-1,-1):
            print("".join([z.Show() for z in self.map_holder[(self.x_max*y):(self.x_max*(y+1))]]))
        print("]")
        