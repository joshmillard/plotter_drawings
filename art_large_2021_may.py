""" hatching an irregularly-proportioned grid of quadrilaterals
    originally created as part of May 2021 patreon monthly patron art output
"""

from cortexdraw import *


def getpolyfield(w=8, h=5, length=10):
    """ generate and return a list of irregular polygons laid out in a checkerboard arrangement """
    newquads = []
    for i in range(w):
        for j in range(h):
            # growth = 0
            growth = (random.random() - 0.5) * 0.5
            x1 = (i - growth) * length
            y1 = (j - growth) * length
            x2 = (i + 1 + growth) * length
            y2 = (j + 1 + growth) * length
            newsq = [[x1, y1], [x1, y2], [x2, y2], [x2, y1]]
            newquads.append(newsq)
    return newquads


def getunevengrid(w=7, h=6, length=10):
    """ generate and return a squared-off grid with random intervals for each row and column"""
    newquads = []

    # generate a set of intervals
    dx = [0]
    dy = [0]

    for i in range(w):
        # dx.append( (random.random() - 0.5)*(length) + length + dx[-1])
        dx.append((random.random() + 0.25) * length + dx[-1])
    for j in range(h):
        # dy.append( (random.random() - 0.5)*(length) + length + dy[-1])
        dy.append((random.random() + 0.25) * length + dy[-1])

    # and then normalize them
    sumx = w * linelength / dx[-1]
    sumy = h * linelength / dy[-1]
    for i in range(len(dx)):
        dx[i] *= sumx
    for i in range(len(dy)):
        dy[i] *= sumy

    # and then turn 'em into squares
    for i in range(w):
        for j in range(h):
            x1 = dx[i]
            y1 = dy[j]
            x2 = dx[i + 1]
            y2 = dy[j + 1]
            newsq = [[x1, y1], [x1, y2], [x2, y2], [x2, y1]]
            newquads.append(newsq)
    return newquads


def getperturbedgrid(w=8, h=7, length=10):
    """ generate and return a connected net of perturbed squares"""
    polys = []
    mag = length * 1
    # generate grid vertices from which net of polygons will be constructed
    points = [None] * (w + 1)
    for i in range(w + 1):
        points[i] = [None] * (h + 1)
        for j in range(h + 1):
            # points[i][j] = [i*len,j*len]
            # do some perturbation...
            points[i][j] = [i * length + (random.random() - 0.5) * mag, j * length + (random.random() - 0.5) * mag]

    # ...and then construct actual polygon objects from vertices
    for i in range(w):
        for j in range(h):
            newsq = [points[i][j], points[i][j + 1], points[i + 1][j + 1], points[i + 1][j]]
            polys.append(newsq)
    return polys


width = 12
height = 9
linelength = 8

# fig = plt.figure()
art = new_artwork()
""" Purpose: create a Figure object onto which one or more axes will be attached
    
    Desired abstraction: put this behind some sort of "new document" function that can be called
    at the top of a script and otherwise not worried about in terms of implementation specifics
    e.g. document = new_document()
"""

#axs = makeaxesgrid(fig, 4)
art = add_layer(art)
art = add_layer(art)
art = add_layer(art)
""" Purpose: create one or more axes which will be attached to parent Figure object
    
    Desired abstraction: make "there's one layer" the default outcome of creating a new document in the
    previous function; provide an "add layer" function that hides implementation details
    e.g. document.add_new_layers(numlayers=1)
"""

# permagrid = getunevengrid(width, height, linelength)
permagrid = getperturbedgrid(width, height, linelength)

# for a in axs:
for a in art.axes:
    count = -50
    patches = []
    quads = copy.deepcopy(permagrid)
    for q in quads:
        count += 1
        q = jitter(q, 2, True)
        # patches.append(mpatches.Polygon(q,closed=True,fill=None, color="black"))
        # hatching = crophatch(q, random.random()*math.pi*0.2, random.random()/4 +.25)
        # if(random.random() > 0.5): continue
        hatching = crophatch(q, random.random() * math.pi, random.random() / (abs(count) + 1) * 50 + .25)
        # hatching = circuitpolyline(q,int(random.random() * 20)+10)
        for line in hatching:
            # if(random.random() > 0.5): continue
            line = jitter(line, 0.1, True)
            patches.append(mpatches.Polygon(line, closed=False, fill=None))
            """ Purpose: add the calculated geometry to a patches object specific to matplotlib's rendering
                
                Desired abstraction: add very primitive geometry types to a simple list of geometric data,
                just line segments and arc definitions and polygons in some simple and intuitive form, and
                then take that stack of object and feed it to a "add_lines()" function that translates that 
                into implementation-specific details for matplotlib.
                
                What is that list of geometric types, and how much flexibility do I need to wrangle them?
            """

    collection = PatchCollection(patches, match_original=True)
    a.add_collection(collection)

x_bounds = [-5, width * linelength + 5]
y_bounds = [-5, height * linelength + 5]
""" Purpose: define where the borders of the drawing are in the same raw coordinates as the geometry being drawn
    
    Desired abstraction: allow for an autocalculated default boundary, either a snug rectangle around the drawn 
    material or something with a proportional border (and really the latter would be derived from the former).
    Naive approach: sort through all vertices and identify the left-, right-, top-, and bottom-most of them. This
    should work fine for straight lines but anything with curves becomes more complex.  
    
    Does there exist library code that will handle this nicely?  Is this something it'd make more sense to just 
    defer to vpype on and not try to get right at this stage in the code?  Downside of *that* is that plt.show() 
    gives matplotlib's rendering, not vpype's.  Perhaps use a viewer to show the rendered SVG after vpype has 
    done its work, instead of plt.show()?
"""

writefigure(art, xbounds=x_bounds, ybounds=y_bounds, name="art_large_2021_may")
