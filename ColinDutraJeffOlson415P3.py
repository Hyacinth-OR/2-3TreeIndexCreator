import tree23 as t
import bst as bst
import re
from operator import itemgetter
import timeit
import sys
sys.setrecursionlimit(90000)

def squash(list): # no longer used in this implementation
    # takes a list of format [[word,line,line,..],...], and gets rid of duplicate words, adding their line nums
    # to the first occurrence of the word in the list.
    copy = list
    curr = 0
    while curr <= len(copy):
        scan = curr + 1
        while scan < len(copy):
            currword, scanword = copy[curr][0], copy[scan][0]
            if currword == scanword:
                copy[curr].append(copy[scan][1])
                copy.pop(scan)

            scan += 1
        curr += 1

    final = []
    for package in copy:
        final.append(cull(package))
    return final





def preprocess(list):
    wordcount = 0
    index = [] # this list will be in format [[word,line,line,..],...]
    for pack in list:
        for word in pack[1:]:
            ln = pack[0]
            indexpack = [word,ln]
            index.append(indexpack)

    #index = squash(index)
    #index = sorted(index, key=itemgetter(0))  ///uncomment to presort words!///
    return index


def isnumber(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def cull(culled): #  removes duplicates from lists
    culled = list(dict.fromkeys(culled).keys())
    return culled


def cullnumber(list):
    no_integers = [x for x in list if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]
    return no_integers

def indexPrint(indexlist):
    for elem in indexlist: # for good formatting
        spacing = 35 - len(elem[0])
        print(elem[0], end ='')
        for i in range(spacing):
            print(' ',end = '')
        lines = []
        for ln in elem[1:]:
            if type(ln) is list:
                lines.append(int(ln[0]))
            else:
                lines.append(int(ln))
        print(lines)

def indexWrite(indexlist,file = "index.txt"):
    file = open(file,"w")
    for elem in indexlist: # for good formatting
        spacing = 35 - len(str(elem[0]))
        file.write(str(elem[0]).rstrip('\n'))
        for i in range(spacing):
            file.write(' '.rstrip('\n'))
        file.write(str(elem[1:]))
        file.write("\n")


def processFile(file):
    infile = open(file, 'r', errors="backslashreplace")
    lines = infile.readlines()
    infile.close()
    outtext = ['%d %s' % (i, line) for i, line in enumerate(lines)]
    outfile = open("linedup.txt", "w")
    outfile.writelines(str("".join(outtext)))
    outfile.close()

    with open("linedup.txt", "r") as file_data:

        line = file_data.read()
        line = re.sub('[!@.()"$%^&+=:;]', '', line)

        linelist = re.split(';|,|\n|\s|--|-', line)

        filelist = []  # a list of lists containing a line number in index 0, followed by all words on that line

        justwords = []  # used for building our trees

        linepack = [0]
        words = 0
        for word in linelist[1:]:
            word = word.upper()
            # print("evaluating",word)
            if word != '' and not isnumber(word):
                # print(word, "is not a number, packing!")
                words +=1
                linepack.append(word)
                justwords.append(word)
            elif isnumber(word):
                # print(word,"is a number! Appending and moving on...")
                filelist.append(linepack)
                #  print(linepack,"appended!")
                linepack = [word]
        filelist.append(linepack)

    return justwords, preprocess(filelist),words

def info(words,dwords,buildtime,height):
    strings = ["Total number of words:","Total number of distinct words:","Total time spent building tree:",
               "Height of Tree is:"]
    info = [words,dwords,buildtime,height]
    for i in range(len(info)):
        spacing = 35 - len(strings[i])
        print(strings[i],end = "")
        for j in range(spacing):
            print(' ',end = "")
        print(info[i])

def main():
    #file = input("Enter name of file.")
    file = "20k.txt"
    justwords, lnwordlist,wordcount = processFile(file)
    #print(len(lnwordlist),len(squash(lnwordlist)))
    while True:
        print("Please select an option:")
        print("Options: (a) BST, (b) 2-3 Tree, (c) Compare BST and 2-3 Tree")
        mode = input().lower()
        if mode == "a":
            start = timeit.default_timer()
            tree = bst.BST()
            tree.buildtree(lnwordlist)
            buildtime = str((timeit.default_timer() - start)) + " seconds"
            opt = 0
            info(wordcount, tree.getSize(), buildtime, tree.getRoot().height())
            while opt != 4:
                print("Options: (1) display index, (2) search, (3) save index, (4) quit\n")
                opt = int(input())
                if opt == 1:
                    inorder = tree.inorder(tree.getRoot())
                    indexPrint(inorder)
                elif opt == 2:
                    word = input("Enter word to find:\n")
                    inorder = tree.inorder(tree.getRoot())
                    for elem in inorder:
                        if elem[0] == word.upper():
                            if tree.find(elem) == True:
                                print(elem[0],"found in tree, it occurs",len(elem[1:]),"time(s) on line(s)",elem[1:])
                elif opt == 3:
                    inorder = tree.inorder(tree.getRoot())
                    indexWrite(inorder)
                    print("Output written to 'index.txt' in project folder.")

                else:
                    break
            exit()

        elif mode == "b":
            start = timeit.default_timer()
            tree = t.Tree()
            tree.buildtree(lnwordlist)

            buildtime = str((timeit.default_timer() - start)) + " seconds."

            info(wordcount,tree.getSize(),buildtime,tree.height())
            opt = 0
            while opt != 4:
                print("Options: (1) display index, (2) search, (3) save index, (4) quit")
                opt = int(input())
                if opt == 1:
                    inorder = tree.inorder([])
                    indexPrint(inorder)

                elif opt == 2:
                    word = input("Enter word to find:\n")
                    inorder = tree.inorder([])
                    for elem in inorder:
                        if elem[0] == word.upper():
                            if tree.get(elem) != None:
                                print(elem[0], "found in tree, it occurs", len(elem[1:]), "time(s) on line(s)", elem[1:])
                elif opt == 3:
                    inorder = tree.inorder([])
                    indexWrite(inorder)
                    print("Output written to 'index.txt' in project folder.")
                else:
                    break
            exit()

        else:
            start1 = timeit.default_timer()
            btree = bst.BST()
            btree.buildtree(lnwordlist)
            for elem in lnwordlist:
                btree.find(elem)
            buildtime1 = str((timeit.default_timer() - start1)) + " seconds."

            start2 = timeit.default_timer()
            tree23 = t.Tree()
            tree23.buildtree(lnwordlist)
            for elem in lnwordlist:
                tree23.get(elem)
            buildtime2 = str((timeit.default_timer() - start2)) + " seconds."

            s1, s2 = "Total time taken by BST:", "Total time taken by 2-3 Tree:"
            sp1,sp2 = 25 - len(s1),25 - len(s2)
            print(s1, end="")
            for i in range(sp1):
                print(' ', end="")
            print(buildtime1)
            print(s2, end="")
            for j in range(2):
                print(' ', end="")
            print(buildtime2)







main()