from DNATreeNode import DNATreeNode
from FlyweightNode import FlyweightNode 
from LeafNode import LeafNode
class InternalNode(DNATreeNode):

    def __init__(self,fw,level):
        self.a = fw
        self.c = fw
        self.g = fw
        self.t = fw
        self.end = fw

        self.setLevel(level)

    def addNode(self,node,pos):
        if(pos == "A"):
            self.a = node
        elif(pos == "C"):
            self.c = node
        elif(pos == "G"):
            self.g = node
        elif(pos == "T"):
            self.t = node 
        elif(pos == "E"):
            self.end = node


    def getNode(self,pos):
        if(pos == "A"):
            return self.a 
        elif(pos == "C"):
            return self.c
        elif(pos == "G"):
            return self.g
        elif(pos == "T"):
            return self.t
        elif(pos == "E"):
            return self.end

        
    
    def getNumFlyNodes(self):
        if( isinstance(self.a, FlyweightNode)):
            numa = 1
        else:
            numa = 0
                
        if( isinstance(self.c, FlyweightNode)):
            numc = 1
        else:
            numc = 0

        if( isinstance(self.g, FlyweightNode)):
            numg = 1
        else:
            numg = 0

        if( isinstance(self.t, FlyweightNode)):
            numt = 1
        else:
            numt = 0
        
        if( isinstance(self.end, FlyweightNode)):
            numend = 1
        else:
            numend = 0

        return numa + numc + numg + numt + numend
        
        
        
                


