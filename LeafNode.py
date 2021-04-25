from DNATreeNode import DNATreeNode
class LeafNode(DNATreeNode):
    def __init__(self,seq,level):
        self.sequence = seq
        self.setLevel(level)


    def getSequence(self):
        return self.sequence