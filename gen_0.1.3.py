import json
import os
import copy
import glob
from PIL import Image, ImageColor, ImageDraw

class Tree():

    storage = []

    def __init__(self, name, init_depth):
        """
        """
        self.name = name
        self.init_depth = init_depth


    def generate(
        self, nodelist=[], index=0, parent=None, root_hue=0,
        binary_switch=0, depth=0, max_children=2, max_depth=2):
        """
        """
        n = 2
        switch_state = '((0 + i) if binary_switch == 0 else (1 - i))'
        nodelist_extend = nodelist.extend([[
                            index + i,
                            parent,
                            self.binary_return(
                                eval(switch_state),
                                hue, hue_len, root_hue
                                ),
                            int((0 + i) if binary_switch == 0 else (1 - i)),
                            depth
                            ] for i in range(n)
                            ])

        if depth < max_depth and depth >=0:
            # add two children
            nodelist_extend

            # for each new child, add two new children
            [self.generate(
                nodelist, len(nodelist), index + i,
                nodelist[index + i][2], nodelist[index + i][3],
                depth + 1, max_children, max_depth)
                for i in range(n)
                ]

        elif depth == max_depth:
            # add two leaves to each max_depth child
            nodelist_extend


    def binary_return(
        self, switch, array, array_len, index):
        """ Return element from x array using modular arithmetic
            :param:     switch      int, selects direction of modular
                                    arithmetic
            :param:     array       list, data to perform modular
                                    arithmetic on
            :param:     array_len   int, length of array
            :param:     index       int, selects index of array
        """
        global interval_input

        # return from ind-th index to (n+i)th index.
        i = index
        if switch == 0:
            counter_clockwise = array[
                ((i - interval_input) % array_len)
                ]
            return counter_clockwise
        elif switch == 1:
            clockwise = array[
                ((i + interval_input) % array_len)
                ]
            return clockwise


    def prune(self, storage=storage):
        temp_storage = []
        with open("{}.txt".format(self.name), "a+") as f:
            for i in range(len(storage)):
                if storage[i][4] == self.init_depth:
                    temp_storage.append(storage[i])
            json.dump(temp_storage, f)
        storage.clear()
        temp_storage.clear()


    def import_pruned(self):
        with open('{}.txt'.format(self.name), 'r') as f:
            self.storage = json.load(f)


    def create_composite_image(self):
        global final
        files = {}
        temp = {}
        count = 0

        for i in range(self.init_depth):
            if count == 0:
                index_create = 0
                for i in range(int(len(self.storage) // 2)):
                    self.create_pair(
                        self.storage[index_create][2],
                        self.storage[index_create + 1][2],
                        self.storage[index_create][3],
                        files, i
                        )
                    index_create += 2

            elif count < self.init_depth and count > 0:
                index_merge = 0
                for i in range(int(len(files) / 2)):
                    self.merge_pairs(
                        0,
                        files['pair_{}'.format(index_merge)],
                        files['pair_{}'.format(index_merge + 1)],
                        temp, i
                        )
                    index_merge += 2

                files.clear()
                files = copy.deepcopy(temp)
                temp.clear()
            count += 1
        self.merge_pairs(
            2,
            files['pair_0'],
            files['pair_0'],
            temp, i
            )



    def create_pair(
        self, px_1_hue='0', px_2_hue='180',
        binary_switch=0, files={}, pair_count=0
        ):
        """Creates 2x2 px Image, adds to dict, then returns dict
            :param:     px_1_hue        str, hue of pixel 1
            :param:     px_2_hue        str, hue of pixel 2
            :param:     binary_switch   int, selects colour order
            :param:     files           list, merged pixel pairs; each
                                              pair is an Image object
            :param:     pair_count      int, tracks and names current
                                             pair
        """
        a = px_1_hue
        b = px_2_hue

        im = Image.new('RGB', (2,2))
        pair_image = ImageDraw.Draw(im)

        if binary_switch == 0:
            colour_1 = 'hsl({},100%,50%)'.format(a)
            colour_2 = 'hsl({},100%,50%)'.format(b)
        elif binary_switch == 1:
            colour_1 = 'hsl({},100%,50%)'.format(b)
            colour_2 = 'hsl({},100%,50%)'.format(a)

        pair_image.point(
            (0,0), fill = colour_1
            )
        pair_image.point(
            (1,0), fill = colour_2
            )
        pair_image.point(
            (0,1), fill = colour_2
            )
        pair_image.point(
            (1,1), fill = colour_1
            )

        pair_index = "pair_" + str(pair_count)
    #    compressed = im.resize((1, 1))
        files[pair_index] = im

        return files


    def merge_pairs(
        self, save, file_1, file_2, temp={}, pair_count=0):
        """Merge two images into one, displayed side by side
            :param:     file1    path to first image file
            :param:     file2    path to second image file
            :return:             the merged Image object
        """
        size = file_1.width
        flipped = file_2.transpose(Image.FLIP_LEFT_RIGHT)
        im = Image.new(
            'RGB', ((size * 2), (size * 2))
            )

        im.paste(
            im = file_1, box = (0, 0)
            )
        im.paste(
            im = flipped, box = (size, 0)
            )
        im.paste(
            im = flipped, box = (0, size)
            )
        im.paste(
            im = file_1, box = (size, size)
            )

        if save == 0:
    #        compressed = im.resize((size,size))
            pair_index = "pair_" + str(pair_count)
            temp[pair_index] = im
        elif save == 1:
            im.save('{}_pair_{}.png'.format(self.name, pair_count))
        elif save == 2:
            pair_index = "{}".format(self.name)
            final[pair_index] = im
        return temp



def deleteTxt():
    for file in glob.glob("*.txt"):
        if os.path.isfile('{}'.format(file)):
            os.remove('{}'.format(file))
        else:
            print("Error: {} file not found".format(file))


def mergeFinal(
    file_1, file_2, temp={}):
    """Merge two images into one, displayed side by side
        :param:     file1    path to first image file
        :param:     file2    path to second image file
        :return:             the merged Image object
    """
    size = file_1.width
    flipped = file_2.transpose(Image.FLIP_LEFT_RIGHT)
    im = Image.new(
        'RGB', ((size * 2), (size * 2))
        )

    im.paste(
        im = file_1, box = (0, 0)
        )
    im.paste(
        im = flipped, box = (size, 0)
        )
    im.paste(
        im = flipped, box = (0, size)
        )
    im.paste(
        im = file_1, box = (size, size)
        )
    im.save('final.png')

def compressResize(file, iter):
    size = iter + 1
    compressed = file.resize((size,size))
    resize = compressed.resize((1024,1024))
    resize.save('{}.png'.format(size))


deleteTxt()

final = {}

hue = []
for i in range(90):
    hue.append(i)
hue_len = len(hue)

depth_input = int(input('Depth?\n: '))
slave_depth = 10
master_depth = (depth_input - slave_depth)
interval_input = int(input('Interval?\n: '))

slaves = {}

master = Tree('master', master_depth)

master.generate(
    nodelist = master.storage, index = len(master.storage), parent = 0,
    root_hue = 0, binary_switch = 0, depth = 1, max_depth = master_depth)
master.prune()
master.import_pruned()
print(master.storage)
print('\n\n')
for i in range(len(master.storage)):

    value = Tree('{}'.format('slave_' + str(i)), slave_depth)
    value.generate(
        nodelist = value.storage, index = len(value.storage),
        parent = master.storage[i][0], root_hue = master.storage[i][2],
        binary_switch = master.storage[i][3], depth = 1,
        max_depth = slave_depth)
    value.prune()
    value.import_pruned()
    value.create_composite_image()
    print(value.storage)
    print('\n\n')
    key = 'slave_' + str(i)
    slaves[key] = value

print(slaves)
#mergeFinal(final['slave_0'], final['slave_1'])
for i in range(1024):
    compressResize(final['slave_0'], i)

deleteTxt()
