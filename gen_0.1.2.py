import os
import copy
from PIL import Image, ImageColor, ImageDraw
from tqdm import tqdm
from pathlib import Path
Image.MAX_IMAGE_PIXELS = 1000000000 

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def generate_binary_tree(
    nodelist=[], idx=0, parent=None, binary_val=0, 
    root_colour=0, root_lightness=12, depth=0, 
    max_children=2, max_depth=2
    ):
    """Build a list of nodes in a binary tree up to a maximum depth.
        :param:    nodelist         list, nodes in the tree; each 
                                          node is a list with 
                                          elements: 
                                        [   idx, 
                                            parent, 
                                            parent_colour, 
                                            binary_val, 
                                            depth, 
                                            colour_string   ]
        :param:    idx              int, index of a node
        :param:    parent           int, index of the node's parent
        :param:    binary_val       int, binary value of a node 
        :param:    root_colour      int, root colour of a node
        :param:    depth            int, distance of a node from 
                                         root
        :param:    max_children     int, maximum number of children 
                                         a node can have
        :param:    max_depth        int, maximum distance from tree 
                                         to root
    """
    n = 2
    switch_state = '((0 + i) if binary_val == 0 else (1 - i))'
    nodelist_extend = nodelist.extend([[
                        idx + i, 
                        parent, 
                        binary_return(
                            2, eval(switch_state), 
                            notes, notes_length, root_colour
                            ), 
                        binary_return(
                            1, eval(switch_state), 
                            lightness, lightness_length, root_lightness
                            ), 
                        int((0 + i) if binary_val == 0 else (1 - i)), 
                        depth, 
                        binary_return(
                            0, eval(switch_state), 
                            notes, notes_length, root_colour
                            ), 
                        binary_return(
                            1, eval(switch_state), 
                            lightness, lightness_length, root_lightness
                            )
                        ] for i in range(n)
                        ]) 
            
    if depth < max_depth and depth >=0:        
        # add two children
        nodelist_extend
        
        # for each new child, add two new children
        [generate_binary_tree(
            nodelist, len(nodelist), idx+i, 
            treecopy[idx+i][4], treecopy[idx+i][2], treecopy[idx+i][3],
            depth+1, max_children, max_depth
            ) for i in range(n)
            ]

    elif depth == max_depth: 
        # add two leaves to each max_depth child
        nodelist_extend


def binary_return( 
    mode, switch, x, y, index):
    """Return element from x array using modular arithmetic 
        :param:     mode    int, selects element from x[]   
        :param:     switch  int, selects direction of modular arithmetic 
        :param:     x       list, data to perform modular arithmetic on
        :param:     y       int, the length of x[]
        :param:     index   int, selects index of x[]
    """   
    global interval_input
    
    # return from ind-th index to (n+i)th index.   
    i = index
    if switch == 0:
        counter_clockwise = x[((i - interval_input) % y)][mode]
        return counter_clockwise
    elif switch == 1:
        clockwise = x[((i + interval_input) % y)][mode]
        return clockwise
        
        
def create_composite_image(
    notes=[], parse_array=[]
    ):
    global depth_input
    global index
    global final_pair
    global final_png
    pair_count = 0
    files = {}
    temp = {}
    index_loop = 0
    index_loop2 = 0
    count = 0
    
    for i in range(depth_input):
        if count == 0:

            for i in range(int(len(parse_array) / 2)):
                create_pair(
                    notes[parse_array[index_loop][2]][1], 
                    lightness[parse_array[index_loop][7]][0],
                    notes[parse_array[index_loop + 1][2]][1],
                    lightness[parse_array[index_loop + 1][7]][0],
                    parse_array[index_loop][4],                   
                    files, pair_count
                    )
                index_loop += 2
                pair_count += 1
            
        elif count < depth_input and count > 0:
            pair_count = 0
            index_place = 0

            for i in range(int(len(files) / 2)):
                
                index_loop2 = "pair_" + str(index_place)
                index_loop3 = "pair_" + str(index_place + 1)
                merge_pairs(
                    0, 
                    files[index_loop2], 
                    files[index_loop3], 
                    pair_count, temp)
                pair_count += 1
                index_place += 2
                
            files.clear()
            files = copy.deepcopy(temp)
            temp.clear()
            index = 0
        count = count + 1
    
    
    
    compress_fractal_alt(files["pair_0"], 540, temp, )
    
    merge_pairs(
        1,
        temp["pair_0"],
        temp["pair_0"],
        0, temp)
    
#    merge_pairs(
#        0,
#        files["pair_0"],
#        files["pair_0"],
#        0, temp)
    
#    compress_fractal(temp["pair_0"], 304)    
    #compress_fractal(temp["pair_0"], 8192)
    #compress_fractal(temp["pair_0"], 4096)

    

def create_pair(
    px_1_hue='0', px_1_lightness='50%', 
    px_2_hue='180', px_2_lightness='50', 
    binary_switch=0, files={}, pair_count=0
    ):
    """Creates 2x2 px Image, adds to dict, then returns dict
        :param:     px_1_hue        str, hue of pixel 1
        :param:     px_1_lightness  str, lightness of pixel 1
        :param:     px_2_hue        str, hue of pixel 2
        :param:     px_2_lightness  str, lightness of pixel 2
        :param:     binary_switch   int, selects colour order
        :param:     files           list, merged pixel pairs; each 
                                          pair is an Image object
        :param:     pair_count      int, tracks and names current
                                         pair   
    """
    a = px_1_hue
    b = px_1_lightness
    c = px_2_hue
    d = px_2_lightness
    global bin_val
    
    im = Image.new('RGB', (2,2))
    pair_image = ImageDraw.Draw(im)
     
    if binary_switch == 0:
        colour_1 = 'hsl({},100%,{})'.format(a, b)
        colour_2 = 'hsl({},100%,{})'.format(c, d)
        bin_val = 0
    elif binary_switch == 1:
        colour_1 = 'hsl({},100%,{})'.format(c, d)
        colour_2 = 'hsl({},100%,{})'.format(a, b)
        bin_val = 1
    
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
    save, file_1, file_2, pair_count=0, temp={}):
    """Merge two images into one, displayed side by side
        :param:     file1    path to first image file
        :param:     file2    path to second image file
        :return:             the merged Image object
    """
    global total_count
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
        im.save(image_folder / ('{}.png'.format(total_count)))
    
        
    
    return temp
        

def compress_fractal(
    file, iter):
    """
    """
    global root_input
    global interval_input
    #image_file = Image.open(file)
    compressed = file.resize((iter, iter))
    
    compressed.save(image_folder / (
        str(interval_input) + '_' + str(root_input) + 'compressed_fractal_' + str(iter) + '.png'
        ))
        
def compress_fractal_alt(
    file, iter, temp={}, pair_count=0):
    """
    """
    global root_input
    global interval_input
    #image_file = Image.open(file)
    compressed = file.resize((iter, iter))
    
    pair_index = "pair_" + str(pair_count) 
    temp[pair_index] = compressed


_notes = [
    ('A', '270', 0), ('A#', '300', 1), ('B', '330', 2), 
    ('C', '0', 3), ('C#', '30', 4), ('D', '60', 5), 
    ('D#', '90', 6), ('E', '120', 7), ('F', '150', 8), 
    ('F#', '180', 9), ('G', '210', 10), ('G#', '240', 11)
    ]
_notes = [
    ('A', '270', 0), ('A#b', '285', 1), ('A#', '300', 2), 
    ('Bb', '315', 3), ('B', '330', 4), ('Cb', '345', 5), 
    ('C', '0', 6), ('C#b', '15', 7), ('C#', '30', 8), 
    ('Db', '45', 9), ('D', '60', 10), ('D#b', '75', 11), 
    ('D#', '90', 12), ('Eb', '105', 13), ('E', '120', 14), 
    ('Fb', '135', 15), ('F', '150', 16), ('F#b', '165', 17), 
    ('F#', '180', 18), ('Gb', '195', 19), ('G', '210', 20), 
    ('G#b', '225', 21), ('G#', '240', 22), ('Ab', '255', 23)
    ]
_lightness = [
    ('0%', 0), ('4%', 1), ('8%', 2), ('12%', 3), ('17%', 4), 
    ('21%', 5), ('25%', 6), ('29%', 7), ('33%', 8), ('37%', 9), 
    ('42%', 10), ('46%', 11), ('50%', 12), ('54%', 13), ('58%', 14), 
    ('63%', 15), ('67%', 16), ('71%', 17), ('75%', 18), ('79%', 19), 
    ('83%', 20), ('88%', 21), ('92%', 22), ('96%', 23), ('100%', 24)
    ]
lightness = [
    ('0%', 0), ('8%', 1), ('17%', 2), ('25%', 3), ('33%', 4), 
    ('42%', 5), ('50%', 6), ('58%', 7), ('67%', 8), ('75%', 9),
    ('83%', 10), ('92%', 11), ('100%', 12)
    ]
notes = []
#lightness = []

notes_count = 0
while notes_count <= 360:
    notes.append(('a', '{}'.format(notes_count), int(notes_count)))
    notes_count += 1

#light_count = 0
#while light_count <= 100:
#    lightness.append(('{}%'.format(light_count), int(light_count)))
#    light_count += 1
    


parse_array = []
notes_length = len(notes)
lightness_length = len(lightness)

temp_folder = Path("temp/")
image_folder = Path("images/")

[(print(
    (str(1 + i) + '. ' + '\t'), 
    notes[i][0])
    ) 
    for i in range(len(notes))
    ]
root_input = int(
    int(input(
        "Select root colour from list (input integer)" 
        + '\n:')) - 1) 
depth_input = int(input("Depth? (input integer between 1 and 12) \n:"))
interval_input = int(input(
    "Interval distance? (input integer between 1 and 12) \n:"
    ))
#input_res = int(input(
#    "Target fractal resolution? (input integer) \n:")
tree = [
    [0, None, root_input, 6, 0, 0, notes[root_input][1], '50%']
    ]
treecopy = [
    [0, None, root_input, 6, 0, 0, notes[root_input][1], '50%']
    ]

total_count = 0
total_depth = 360
for i in tqdm(range(total_depth)):
    generate_binary_tree(
        nodelist = treecopy, idx = len(treecopy), parent = 0, binary_val = 0, 
        root_colour = root_input, root_lightness = 6, depth = 1, 
        max_children = 3, max_depth = depth_input
        )
    count = 0
#    with open("{}.txt".format(total_count), "a+") as f:
    while count != len(treecopy):       
        count = count + 1
        if count <= len(treecopy) - 1:
            if treecopy[count][5] == depth_input:
                #f.write(', '.join([str(x) for x in treecopy[count]]))
                #f.write('\n')
                parse_array.append(treecopy[count])    
        
    create_composite_image(notes, parse_array)
    parse_array.clear()
    treecopy.clear()
    treecopy = copy.deepcopy(tree)
    root_input = binary_return(2, 1, notes, notes_length, root_input)
    #interval_input += 1
    total_count += 1
    

#compress_fractal(), 8192)
#compress_fractal(image_folder / ('final.png'), 2048)
#compress_fractal(image_folder / ('final.png'), 4096)
#compress_fractal(image_folder / ('final.png'), 512)


#print(notes_test)
input("end")