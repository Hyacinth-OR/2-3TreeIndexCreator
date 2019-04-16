



def make1d(twoD): # strip some unnecessary formatting
    oneD = []
    for elem in twoD:
        if type(elem[0]) is not list:
            elem = [elem]
        if type(elem) is str:
            oneD.append(elem)
        else:
            for subelem in elem:
                oneD.append(subelem)

    return oneD

class Node:
    def __init__(self, data, par=None):
        self.data = list([data])
        self.parent = par
        self.children = list()


    def __lt__(self, node):
        return self.data[0][0] < node.data[0][0]

    def _add(self, node):
        for children in node.children:
            children.parent = self

        self.data.extend(node.data)
        self.datasort()
        self.children.extend(node.children)

        if len(self.children) > 1:
            self.children.sort()
        if len(self.data) > 2:
            self._split()

    def _insert(self, node):

        if len(self.children) == 0:
            self._add(node)

        elif node.data[0][0] > self.data[-1][0]:
            self.children[-1]._insert(node)

        elif node.data[0][0] == self.data[0][0]:
            self.data[0].append(node.data[0][1:])

        elif node.data[0][0] == self.data[-1][0]:
            self.data[-1].append(node.data[0][1:])



        else:
            for i in range(0, len(self.data)):
                if node.data[0][0] < self.data[i][0]:
                    self.children[i]._insert(node)
                    break

    def _split(self):
        Lchildren = Node(self.data[0], self)
        Rchildren = Node(self.data[2], self)
        if self.children:
            self.children[0].parent = Lchildren
            self.children[1].parent = Lchildren
            self.children[2].parent = Rchildren
            self.children[3].parent = Rchildren

            Lchildren.children = [self.children[0], self.children[1]]
            Rchildren.children = [self.children[2], self.children[3]]

        self.children = [Lchildren]
        self.children.append(Rchildren)
        self.data = [self.data[1]]

        if self.parent:
            if self in self.parent.children:
                self.parent.children.remove(self)
            self.parent._add(self)

        else:
            Lchildren.parent = self
            Rchildren.parent = self

    def _get(self, item):
        if item in self.data:
            return item
        elif len(self.children) == 0:
            return False
        elif item > self.data[-1]:
            return self.children[-1]._get(item)
        else:
            for i in range(len(self.data)):
                if item < self.data[i]:
                    return self.children[i]._get(item)

    def _height(self):
        height = 0
        try:
            lh = self.children[0]._height()
            lh += 1
        except IndexError:
            lh = 0

        try:
            mh = self.children[1]._height()
            mh += 1
        except IndexError:
            mh = 0

        try:
            rh = self.children[2]._height()
            rh += 1
        except IndexError:
            rh = 0

        return height + max(lh,mh,rh)

    def _getSize(self):
        if self is None:
            return 0
        elif len(self.children) == 0:
            return len(self.data)

        elif(len(self.children)) == 1:
            return (self.children[0]._getHeight() + len(self.data))

        elif(len(self.children) == 2):
            return (self.children[0]._getSize() + len(self.data) + self.children[-1]._getSize())

        else:
            return (self.children[0]._getSize() + len(self.data) + self.children[-1]._getSize() +
                    self.children[1]._getSize())

    def datasort(self):
        self.data.sort(key = lambda x: x[0])

    def _inorder(self,holder):

        if self is None:
            return holder

        if len(self.children) == 0:
            holder.append(self.data)

        elif len(self.children) == 2:
            self.children[0]._inorder(holder)
            holder.append(self.data)
            self.children[1]._inorder(holder)

        elif len(self.children) == 3:
            self.children[0]._inorder(holder)
            holder.append(self.data[0])
            self.children[1]._inorder(holder)
            holder.append(self.data[1])
            self.children[2]._inorder(holder)

        return holder



class Tree:
    def __init__(self):
        self.root = None
        self.size = 0

    def buildtree(self,list):
        for elem in list:
            #print("inserting",elem)
            self.insert(elem)

    def getSize(self):
        return self.size

    def insert(self, item):
        if self.root is None:
            self.root = Node(item)
        else:
            self.root._insert(Node(item))
            while self.root.parent:
                self.root = self.root.parent
        return True

    def get(self, item):
        return self.root._get(item)

    def height(self):
        return self.root._height()

    def getSize(self):
        return self.root._getSize()

    def inorder(self,holder):
        return make1d(self.root._inorder(holder))



