def striplist(inorder):
    stripped = []
    for elem in inorder:
        pack = []
        pack.append(list(inorder[0]))
        for ln in elem[1:]:
            lns = []
            lns.append(str(ln))
        pack.append(lns)
        stripped.append(pack)
    return stripped


class Node:
    def __init__(self, val):
        self.val = list(val)
        self.left = None
        self.right = None

    def __lt__(self, node):
        return self.val[0] < node.val[0]

    def __eq__(self,node):
        return self.val[0] == node.val[0]

    def __gt__(self,node):
        return self.val[0] > node.val[0]

    def get(self):
        return self.val
    
    def set(self, val):
        self.val = val
        
    def getChildren(self):
        children = []
        if(self.left != None):
            children.append(self.left)
        if(self.right != None):
            children.append(self.right)
        return children

    def height(self):
        if self.right is None and self.left is None:
            return 0
        elif self.right is None and self.left is not None:
            return self.left.height() + 1
        elif self.right is not None and self.left is None:
            return self.right.height() + 1

        else:
            return 1 + max(self.right.height(), self.left.height())

        
class BST:
    def __init__(self):
        self.root = None
        self.size = 0

    def setRoot(self, val):
        self.root = Node(val)

    def insert(self, val):
        if(self.root is None):
            self.setRoot(val)
            self.size += 1

        else:
            self.insertNode(self.root, val)


    def insertNode(self, currentNode, val):
        if(val[0] < currentNode.val[0]):
            if(currentNode.left):
                self.insertNode(currentNode.left, val)
            else:
                nn = Node(val)
                currentNode.left = nn
                self.size += 1

        elif(val[0] == currentNode.val[0]):
            currentNode.val.append(val[1:])

        elif(val[0] > currentNode.val[0]):
            if(currentNode.right):
                self.insertNode(currentNode.right, val)
            else:
                nn = Node(val)
                currentNode.right = nn
                self.size += 1

    def buildtree(self,list):
        for elem in list:
            self.insert(elem)

    def inorder(self, root):
        res = []
        if root:
            res = self.inorder(root.left)
            res.append(root.val)
            res = res + self.inorder(root.right)
        return res

    def find(self, val):
        return self.findNode(self.root, val)

    def getRoot(self):
        return self.root

    def getSize(self):
        return self.size

    def findNode(self, currentNode, val):
        if(currentNode is None):
            return False
        elif(val[0] == currentNode.val[0]):
            return True
        elif(val[0] < currentNode.val[0]):
            return self.findNode(currentNode.left, val)
        else:
            return self.findNode(currentNode.right, val)