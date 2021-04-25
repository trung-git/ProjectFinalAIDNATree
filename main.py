import re
import sys
from DNATreeNode import DNATreeNode
from FlyweightNode import FlyweightNode
from InternalNode import InternalNode
from LeafNode import LeafNode
from DNATree import DNATree


class main:
    INSERT_PATTERN = "^ *(insert|INSERT) *[ACGT]+ *$"
    REMOVE_PATTERN = "^ *(remove|REMOVE) *[ACGT]+ *$"
    PRINT_PATTERN = "^ *(print|PRINT) *$"
    PRINT_LENGTHS_PATTERN = "^ *(print|PRINT) *(lengths|LENGTHS) *$"
    PRINT_STATS_PATTERN = "^ *(print|PRINT) *(stats|STATS) *$"
    SEARCH_PATTERN = "^ *(search|SEARCH) *[ACGT]+[$]? *$"


def main():
    INSERT_PATTERN = "^ *(insert|INSERT) *[ACGT]+ *$"
    REMOVE_PATTERN = "^ *(remove|REMOVE) *[ACGT]+ *$"
    PRINT_PATTERN = "^ *(print|PRINT) *$"
    PRINT_LENGTHS_PATTERN = "^ *(print|PRINT) *(lengths|LENGTHS) *$"
    PRINT_STATS_PATTERN = "^ *(print|PRINT) *(stats|STATS) *$"
    SEARCH_PATTERN = "^ *(search|SEARCH) *[ACGT]+[$]? *$"

    if(len(sys.argv) != 2):
        print("Moi nhap : python main.py [inputfile]")
        return
    else:
        file = sys.argv[1]
        f = open(file, "r")
        lines = f.readlines()
        tree = DNATree()
        for line in lines:
            if(re.match(INSERT_PATTERN, line)):
                sequence = line.split()[1]
                result = tree.insert_s1(sequence)
                if(result < 0):
                    print("Sequence " + sequence + " already in tree.")
                else:
                    print("Sequence " + sequence + " inserted at level " , result , ".")
            elif(re.match(REMOVE_PATTERN, line)):
                sequence = line.split()[1]
                temp = tree.remove(sequence) 
                if(temp == False):
                    print("Sequence " + sequence + " not found in tree.")
                else:
                    print("remove done ", sequence)
            elif(re.match(PRINT_PATTERN, line)):
                print(line, " hop le voi PRINT")
                print(tree.print_s1(False, False))
            elif(re.match(PRINT_LENGTHS_PATTERN, line)):
                print(line, " hop le voi PRINT_LENG")
                print(tree.print_s1(True, False))
            elif(re.match(PRINT_STATS_PATTERN, line)):
                print(line, " hop le voi PRINT_STAT")
                print(tree.print_s1(False, True))
            elif(re.match(SEARCH_PATTERN, line)):
                print(line, "hop le voi SEARCH")
                sequence = line.split()[1]
                print(tree.search(sequence))
            else:
                continue


main()
