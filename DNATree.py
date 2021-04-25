from DNATreeNode import DNATreeNode
from FlyweightNode import FlyweightNode
from InternalNode import InternalNode
from LeafNode import LeafNode


class DNATree:
    def __init__(self):
        self.fw = FlyweightNode()
        self.root = self.fw

    def insert_s1(self, sequence):
        if (isinstance(self.root, FlyweightNode)):
            """ print("[insert_s1] if root FW") """
            self.root = LeafNode(sequence, 0)
            return 0
        if(isinstance(self.root, LeafNode)):
            """ print("[insert_s1] if root LN") """
            if(self.root.getSequence() == sequence):
                return -1

            temp = InternalNode(self.fw, 0)
            temp.addNode(self.root, self.root.getSequence()[0])
            self.root.setLevel(1)
            """ temp.getNode(self.root.getSequence()[0]).setLevel(1) """
            self.root = temp
        """ print("[insert_s1] if root IN") """
        return self.insert_s2(sequence, self.root)

    def insert_s2(self, sequence, node):
        if(node.getLevel() < len(sequence)):
            """ print("[insert_s2] node.getLevel() < sequence.length()") """
            position = sequence[node.getLevel()]
        else:
            """ print("[insert_s2] position = 'E';") """
            position = "E"

        child = node.getNode(position)

        if(isinstance(child, FlyweightNode)):
            """ print("child instanceof FlyweightNode") """
            node.addNode(LeafNode(sequence, node.getLevel() + 1), position)
            return node.getLevel()+1

        if(isinstance(child, LeafNode)):
            """ print("child instanceof LeafNode") """
            if(child.getSequence() == sequence):
                """ print("[insert_s2] if (((LeafNode) child).getSequence().equals(sequence)) {") """
                return -1
            """ print("[insert_s2] Replace leaf node with internal node and downshift") """
            temp = InternalNode(self.fw, child.getLevel())
            temp.addNode(child, child.getSequence()[child.getLevel()])
            child.setLevel(child.getLevel() + 1)
            node.addNode(temp, sequence[node.getLevel()])
            child = temp

        return self.insert_s2(sequence, child)

    def remove(self, sequence):
        if (isinstance(self.root, FlyweightNode)):
            return False

        if(isinstance(self.root, LeafNode)):
            if(self.root.getSequence() == sequence):
                self.root = self.fw
                return True
            return False
        return self.findAndRemove(sequence, self.root)

    def findAndRemove(self, sequence, node):
        if(node.getLevel() >= len(sequence)):
            character = "E"
        else:
            character = sequence[node.getLevel()]
        
        nextNode = node.getNode(character)
        if (isinstance(nextNode, FlyweightNode)):
            return False

        if(isinstance(nextNode, LeafNode)):
            if(nextNode.getSequence() == sequence):
                node.addNode(self.fw, character)
                
                return True
            return False

        if(self.findAndRemove(sequence, nextNode) == True):
            if(nextNode.getNumFlyNodes() == 4):
                
                chars = ["A", "C", "G", "T", "E"]
                for currentChar in chars:
                    
                    child = nextNode.getNode(currentChar)
                    
                    if (isinstance(child, LeafNode)):
                        node.addNode(child, character)
                        child.setLevel(child.getLevel()-1)
                        return True
            return True
        return True

    def print_s1(self, lengths, stats):
        if (isinstance(self.root, FlyweightNode)):
            return "Print called on empty tree."

        return self.print_s2(self.root, None, lengths, stats) + "\n"

    def print_s2(self,node, parent, lengths, stats):
        output = "\n"

        if(isinstance(node, FlyweightNode)):
            level = parent.getLevel() + 1
        else:
            level = node.getLevel()

        for i in range(0, level):
            output = output + "  "

        if (isinstance(node, FlyweightNode)):
            output = output + "E"
        elif (isinstance(node, LeafNode)):
            sequence = node.getSequence()
            output = output + sequence
            if(lengths == True):
                output = output + ": length " + str(len(sequence))

            if(stats == True):
                letters = []
                frequencies = []
                for i in range(0, 4):
                    letters.append(0)

                for c in sequence:
                    if(c.lower() == "a"):
                        letters[0] = letters[0] + 1
                    elif(c.lower() == "c"):
                        letters[1] = letters[1] + 1
                    elif(c.lower() == "g"):
                        letters[2] = letters[2] + 1
                    elif(c.lower() == "t"):
                        letters[3] = letters[3] + 1
                for i in range(4):
                    frequencies.append((100.0 * letters[i]) / len(sequence))

                output = output + ": "
                output = output + "A(" + str(round(frequencies[0],2)) + "), "
                output = output + "C(" + str(round(frequencies[1],2)) + "), "
                output = output + "G(" + str(round(frequencies[2],2)) + "), "
                output = output + "T(" + str(round(frequencies[3],2)) + ")"
        else:
            output = output + "I"
            output = output + self.print_s2((node).getNode('A'), node, lengths, stats)
            output = output + self.print_s2((node).getNode('C'), node, lengths, stats)
            output = output + self.print_s2((node).getNode('G'), node, lengths, stats)
            output = output + self.print_s2((node).getNode('T'), node, lengths, stats)
            output = output + self.print_s2((node).getNode('E'), node, lengths, stats)
        return output

    def search(self,pattern):
        if (isinstance(self.root, FlyweightNode)):
            return "Search called on empty tree."

        output = "\n"
        visited = []
        visited.append(1)

        if(pattern[len(pattern) - 1] == "$"):
            exact = True
            pattern = pattern[0:len(pattern) - 1]
        else:
            exact = False
        
        if (isinstance(self.root, LeafNode)):
            sequence = self.root.getSequence()
            if(exact == False and sequence[0:len(pattern)] == pattern):
                output = output + "Sequence: " + pattern
            elif(exact == True and sequence == pattern):
                output = output + "Sequence: " + pattern
            else:
                output = output + "No sequence found"
        else:
            count = 0
            focus = self.root
            while(count < len(pattern)):
                if(isinstance(focus.getNode(pattern[count]), InternalNode)):
                    focus = focus.getNode(pattern[count])
                else: 
                    break
                count = count + 1
                visited[0] = visited[0] + 1 
            if(count == len(pattern)):
                position = "E"
            else:
                position = pattern[count]
            
            nextNode = focus.getNode(position)

            if(exact == True):
                if(isinstance(nextNode, LeafNode) and nextNode.getSequence() == pattern):
                    output = output + "Sequence: " + nextNode.getSequence()
                else:
                    output = output + "No sequence found"
                
                visited[0] = visited[0] + 1
            else:
                if(position != "E" and isinstance(nextNode, LeafNode) and nextNode.getSequence()[0:len(pattern)] == pattern):
                    output = output + "Sequence: " + nextNode.getSequence()
                    visited[0] = visited[0] + 1
                elif(position == "E"):
                    output = output + self.printAllLeafNodes(focus, visited)
                    visited[0] = visited[0] - 1
                    output = output[0:len(output) - 1]
                else:
                    output = output + "No sequence found"
                    visited[0] = visited[0] + 1
        
        return "Number of nodes visited: " + str(visited[0]) + output + "\n"



            


    def printAllLeafNodes(self,node, visited):
        visited[0] = visited[0] + 1
        output = ""

        if(isinstance(node.getNode("A"), LeafNode)):
            output = output + "Sequence: " + node.getNode("A").getSequence() + "\n"
            visited[0] = visited[0] + 1
        elif(isinstance(node.getNode("A"), InternalNode)):
            output = output + self.printAllLeafNodes(node.getNode("A"), visited)
        else:
            visited[0] = visited[0] + 1

        if(isinstance(node.getNode("C"), LeafNode)):
            output = output + "Sequence: " + node.getNode("C").getSequence() + "\n"
            visited[0] = visited[0] + 1
        elif(isinstance(node.getNode("C"), InternalNode)):
            output = output + self.printAllLeafNodes(node.getNode("C"), visited)
        else:
            visited[0] = visited[0] + 1
        
        if(isinstance(node.getNode("G"), LeafNode)):
            output = output + "Sequence: " + node.getNode("G").getSequence() + "\n"
            visited[0] = visited[0] + 1
        elif(isinstance(node.getNode("G"), InternalNode)):
            output = output + self.printAllLeafNodes(node.getNode("G"), visited)
        else:
            visited[0] = visited[0] + 1

        if(isinstance(node.getNode("T"), LeafNode)):
            output = output + "Sequence: " + node.getNode("T").getSequence() + "\n"
            visited[0] = visited[0] + 1
        elif(isinstance(node.getNode("T"), InternalNode)):
            output = output + self.printAllLeafNodes(node.getNode("T"), visited)
        else:
            visited[0] = visited[0] + 1

        if(isinstance(node.getNode("E"), LeafNode)):
            output = output + "Sequence: "+ node.getNode("E").getSequence() + "\n"

        visited[0] = visited[0] + 1

        return output