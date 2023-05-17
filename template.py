""" A minimal example drawing file to demonstrate/test basic use of cortexlib.py """

from cortexdraw import *


def get_grid_of_squares(w=8, h=5, length=10):
    """ generate and return a w*h grid of squares """
    newsquares = []
    for i in range(w):
        for j in range(h):
            growth = (random.random() - 0.5) * 0.5
            x1 = (i - growth) * length
            y1 = (j - growth) * length
            x2 = (i + 1 + growth) * length
            y2 = (j + 1 + growth) * length
            newsq = [[x1, y1], [x1, y2], [x2, y2], [x2, y1]]
            newsquares.append(newsq)
    return newsquares


# establish some arbitrary-to-the-drawing dimensional values for the drawing
width = 12
height = 9
linelength = 10

# create a new artwork with a single layer
art = new_artwork()

# add some more layers for additional distinct drawing passes
art = add_layer(art)
art = add_layer(art)
art = add_layer(art)

# generate some geometry with a drawing function and store it
squares = get_grid_of_squares(width, height, linelength)

# do something with for each layer of the drawing
for a in art.axes:
    patches = []
    quads = copy.deepcopy(squares)
    for q in quads:
        hatching = crophatch(q, random.random() * math.pi + 0.1, random.random() * math.pi + 0.1)
        for line in hatching:
            patches.append(mpatches.Polygon(line, closed=False, fill=None))

    collection = PatchCollection(patches, match_original=True)
    a.add_collection(collection)

x_bounds = [-5, width * linelength + 5]
y_bounds = [-5, height * linelength + 5]

writefigure(art, xbounds=x_bounds, ybounds=y_bounds, name="template")
