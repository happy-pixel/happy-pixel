class Tree():

    storage = []

    def __init__(self, name):
        """
        """
        self.name = name



    def generate(self, nodelist=storage, index=0, parent=None, depth=0, max_children=2, max_depth=2):
        """
        """
        n = 2
        nodelist_extend = nodelist.extend([[
            index + i,
            parent,
            depth
        ] for i in range(n)])

        if depth < max_depth and depth >= 0:
            # add two children
            nodelist_extend

            # for each new child, add two new children
            [self.generate(nodelist, len(nodelist), index + i, depth + 1, max_children, max_depth) for i in range(n)]

        elif depth == max_depth:
            # add two leaves to each max_depth child
            nodelist_extend
            print('hello')


arr = [0, None, 0]
tree = Tree('tree')

tree.generate()
print(tree.storage)
