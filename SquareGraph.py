from collections import defaultdict
import itertools
import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

class MoveDict:
    """ shorthand conversion for all legal moves """
    
    def __init__(self):
        
        self.MD = {
            #no blockers
            "OOO": [],
            #block all directions 
            "BBB": [(1, -1), (1, 0), (1, 1), (0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1)],
            #only one direction blocked 
            #
            "BNN": [(0,1)],
            "BNE": [(1,1)],
            "BEE": [(1,0)],
            "BSE": [(1,-1)],
            "BSS": [(0,-1)],
            "BSW": [(-1,-1)],
            "BWW": [(-1,0)],
            "BNW": [(-1,1)],
        }
        
        #Build up move complex cases open except one side 
        self.MD['BN'] = self.MD["BNW"] + self.MD["BNN"] + self.MD["BNE"] 
        self.MD["BE"] = self.MD["BNE"] + self.MD["BEE"] + self.MD["BSE"]
        self.MD["BS"] = self.MD["BSW"] + self.MD["BSS"] + self.MD["BSE"]
        self.MD["BW"] = self.MD["BNW"] + self.MD["BWW"] + self.MD["BSW"]

        #Passageway,strict
        self.MD["PNS"] = self.MD["BE"]  + self.MD["BW"]
        self.MD["PWE"] = self.MD["BN"]  + self.MD["BS"]
        self.MD["PX"]  = self.MD["BNN"] + self.MD["BEE"] + self.MD["BSS"] + self.MD["BWW"]
        self.MD["P+"]  = self.MD["BNW"] + self.MD["BSW"] + self.MD["BNE"] + self.MD["BSE"]

        #corner,strict
        self.MD["CNW"] = list(set(self.MD['BW'] + self.MD["BN"]))
        self.MD["CNE"] = list(set(self.MD['BN'] + self.MD["BE"]))
        self.MD["CSE"] = list(set(self.MD['BS'] + self.MD["BE"]))
        self.MD["CSW"] = list(set(self.MD['BS'] + self.MD["BW"]))
        
        #capped on three sides, strict.  O referes to the Open Side
        self.MD["ON"] =  list(set(self.MD["BE"] + self.MD["BS"] + self.MD["BW"]))
        self.MD["OE"] =  list(set(self.MD["BN"] + self.MD["BS"] + self.MD["BW"]))
        self.MD["OS"] =  list(set(self.MD["BN"] + self.MD["BE"] + self.MD["BW"]))
        self.MD["OW"] =  list(set(self.MD["BN"] + self.MD["BE"] + self.MD["BS"]))

class Square:
    """ all the properties of each square of the battlefield
    """
    
    def __init__(self,x,y,z=1,d=5,b="OOO",n=None,c=None,l="w"):
        """declare initalization
        
        Attributes:
            x=x coordiante (low = east, high=west)
            y=y coordinate (low = south, high=north)
            z=z coordinate (elevation)
            d=difficulty to move through
            b=blockers
            n=name of cell
            c=actor/character occupying the cell
            l = color (matplotlib colors)
               * blue = b, * green = g, * red =r, * cyan = c, * mauve = m, * yellow =y, * black=k, * white=w
            
        """
        
        self.x = x
        self.y = y
        self.z = z
        self.d = d
        self.b = b
        self.n = str(self.x)+"_"+str(self.y)
        self.c = c
        self.l = l
        self.MoveDict=None
        
        
    def Show(self):
        """ print all features in easy to consume way"""
        return ("(x="+str(self.x)+", y="+str(self.y)+", b="+'"'+str(self.b)+'",'+'l="'+str(self.l)+'"),')
        
class SquareGraph:
    """makes maps
    """
    
    def __init__(self,SquareList,CharacterList =None ):
        """declare initalization

        Attributes:
            SquareList = list of cells
        """
        self.SquareList = SquareList
        self.CharacterList = CharacterList
        
        #graph object, for movememt 
        self.G = nx.Graph()
        
        #graph object for information
        self.SquareGraph = defaultdict(dict)
        for s in self.SquareList:
            self.SquareGraph[s.x][s.y] = s
    
    def MakeMap(self):
        """populate nodes and edges of graph"""
        
        #move Dict
        MD = MoveDict().MD
        
        #add nodes
        [self.G.add_node(s.n) for s in self.SquareList]
             
        #get list of nodes coordinates 
        node_list = [(s.x,s.y) for s in self.SquareList]
        
        #add edges 
        for s in self.SquareList:
            
            #iterate through all sets surrounding 
            for x in [-1,0,1]:
                for y in [-1,0,1]:
                    
                    #if own spot, skip
                    if x == 0 and y==0:
                        continue
                        
                    #validate spot possible on map
                    if (s.x+x,s.y+y) in node_list:
                        
                        #for eligible moves make sure you can leave from current spot
                        if (x,y) not in MD[s.b]:
                            
                            #for eligible moves make sure you can proceed to next space
                            if (-1*x,-1*y) not in MD[self.SquareGraph[s.x+x][s.y+y].b]:
                                
                                #add edge
                                self.G.add_edge(s.n,
                                                self.SquareGraph[s.x+x][s.y+y].n,
                                                
                                                #distance into the next square
                                                #mean to make distances symatric regardless in which way it is built
                                                length=np.mean([self.SquareGraph[s.x+x][s.y+y].d,
                                                                self.SquareGraph[s.x][s.y].d])
                                               )
        #populate make with creatures
        for c in self.CharacterList:
            self.SquareGraph[c.x][c.y].c= c.icon

    def ShowMap(self,SaveFig=False,SaveName=None,PlotGraph=True,dpi=200):
        """visualize map snapshot in time"""
        
        #figure dimensions
        #70 pixels per one square on base settings
        # x /dpi = number of pixels
        x_len = (np.max([s.x for s in self.SquareList]) - np.min([s.x for s in self.SquareList])) * 35/48
        y_len = (np.max([s.y for s in self.SquareList]) - np.min([s.x for s in self.SquareList])) * 35/48
        plt.figure(figsize=(x_len,y_len),frameon=False)
        
        
        #get latest position of all nodes
        pos = {x:np.array([int(x.split("_")[0]),int(x.split("_")[1])]) for x in self.G.nodes}
        
        #draw outlines are barriers 
        for s in self.SquareList:
            
            #get the move dict based on the sides 
            MD = MoveDict().MD
            
            #get the blocked sides 
            blocked = MD[s.b]
            
            #iterate through blocked and plot each corner
            for b in blocked:
                
                #BNN
                if b == (0,1):
                    plt.plot([s.x-0.25,s.x+0.25],[s.y+0.5,s.y+0.5],"k")
                    
                #BNE
                elif b ==(1,1):
                    plt.plot([s.x+0.25,s.x+0.5,s.x+0.5],[s.y+0.5,s.y+0.5,s.y+0.25],"k")
                #BEE
                elif b ==(1,0):
                    plt.plot([s.x+0.5,s.x+0.5],[s.y+0.25,s.y-0.25],"k")
                #BSE
                elif b ==(1,-1):
                    plt.plot([s.x+0.5,s.x+0.5,s.x+0.25],[s.y-0.25,s.y-0.5,s.y-0.5],"k")
                #BSS
                elif b ==(0,-1):
                    plt.plot([s.x-0.25,s.x+0.25],[s.y-0.5,s.y-0.5],"k")
                #BSW
                elif b ==(-1,-1):
                    plt.plot([s.x-0.25,s.x-0.5,s.x-0.5],[s.y-0.5,s.y-0.5,s.y-0.25],"k")
                #BWW
                elif b ==(-1,0):
                    plt.plot([s.x-0.5,s.x-0.5],[s.y-0.25,s.y+0.25],"k")
                #BNW
                elif b ==(-1,1):
                    plt.plot([s.x-0.5,s.x-0.5,s.x-0.25],[s.y+0.25,s.y+0.5,s.y+0.5],"k")
                    
            #plot with color in square, unless white
            if s.l != "w":
                plt.fill_between(x=[s.x-0.5,s.x+0.5],
                                     y1=[s.y-0.5],
                                     y2=[s.y+0.5],
                                     color=s.l)

            
            
        #draw network of map and nodes
        if PlotGraph == True:
            nx.draw(self.G, 
                pos,
                with_labels=True, 
                connectionstyle='arc3, rad = 0.1',
                node_color="#FFFFFF", 
                alpha=1.0, 
                node_size=350, 
                node_shape='s',
                font_color="blue",
                edge_color="red")
            
        #draw characters, in latest position 
        for c in self.CharacterList:
            c.Plot()
        
        #tighten, remove all margin
        plt.subplots_adjust(left=0,right=1.0,top=1.0,bottom=0.0)
        
        #no axis
        plt.axis('off')
        
        #save
        if SaveFig==True and SaveName != "":
            plt.savefig(SaveName,dpi=dpi)
              
    def IterateMap(self):
        """every creature in the map takes their next turn, record of actions"""
        
        #evaluate if multiple teams still standing
        if len([x.team for x in self.CharacterList if x.general_status != "deceased"]) in [0,1]:
            return "Combat Ended"
        
        #evaluate if a creature has a target or not
        for i,_ in enumerate(self.CharacterList):
            print(i)
        
            #indicate if we need to repoint or not
            repoint = False
            
            if ((self.CharacterList[i].x_target == None) or (self.CharacterList[i].y_target == None)):
                repoint = True
            else:
                if self.SquareGraph[self.CharacterList[i].x_target][self.CharacterList[i].y_target] == None:
                    repoint = True
            
            #repoint character if needed
            if repoint:
                
                #find distance to all enemies 
                eDict = {}
                
                for e in self.CharacterList:
                    
                    #only look at enemies 
                    if e.team != self.CharacterList[i].team:
                        eDict[str(e.x)+"_"+str(e.y)]=nx.shortest_path_length(self.G,
                                                        str(self.CharacterList[i].x)+"_"+str(self.CharacterList[i].y),
                                                        str(e.x)+"_"+str(e.y),
                                                        weight="length")
                #choose the closest one
                #ties are broken by random selection
                enemy_location = np.random.choice(list({k:v for k,v in eDict.items() if v == min(set(eDict.values()))}.keys()))
                
                #assign target to location
                self.CharacterList[i].x_target = int(enemy_location.split("_")[0])
                self.CharacterList[i].y_target = int(enemy_location.split("_")[1])
            
            #move action - have character proceed towards opponent
            #determine current location and target, and path between
            sp = nx.shortest_path(self.G,
                                  str(self.CharacterList[i].x)+"_"+str(self.CharacterList[i].y),
                                  str(self.CharacterList[i].x_target)+"_"+str(self.CharacterList[i].y_target),
                                  weight="length")
            
            #only movememt if there are spaces to go exlucding current spot and target spot
            if len(sp) > 2:
                
                #snip off current location and target location
                sp = sp[1:-1]
                
                #proceed until cannot move into
                total_speed_budget = self.CharacterList[i].speed
                
                #attemp to increment
                for s in sp:
                    
                    #find the distance to the next node
                    distance = self.G[str(self.CharacterList[i].x)+"_"+str(self.CharacterList[i].y)][s]["length"]

                    #if can make it to the next node proceed 
                    if distance<=total_speed_budget:
                        
                        #drop original spot
                        self.SquareGraph[self.CharacterList[i].x][self.CharacterList[i].y] = None
                        
                        #update creature
                        self.CharacterList[i].x = int(s.split("_")[0])
                        self.CharacterList[i].y = int(s.split("_")[1])
                        
                        #update map
                        self.SquareGraph[self.CharacterList[i].x][self.CharacterList[i].y] = self.CharacterList[i].icon
                        
                        #update distance
                        total_speed_budget =-distance
                    
                    #else, stop movememt
                    else:
                        break
            #attack