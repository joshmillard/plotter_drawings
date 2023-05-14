# a sketch area

from cortexdraw import *

w = 15
h = 20
s = 7

#patches += draw_circuitgradient(w,h,s)
#patches += draw_grid(w,h,s)

''' # pools of light
#cx = random.random()*w
#cy = random.random()*h
cx = 2.5
cy = 5.5
patches += draw_pooloflight(w,h,s,cx,cy)
patches += draw_pooloflight(w,h,s,cx+random.random()*0.5,cy)
patches += draw_pooloflight(w,h,s,cx,cy+random.random()*0.5)
patches += draw_pooloflight(w,h,s,cx+random.random()*0.5,cy+random.random()*0.5)
#patches += draw_pooloflight(w,h,s,1.1)
#patches += draw_pooloflight(w,h,s,5.1)
'''


''' # line branching willow thing
patches += draw_linebranch(w*s,h*s,30)
'''


''' drawing checkered hatches
#patches += draw_checkerhatch(w,h,s)
'''

#patches += draw_crookedirregularspiral(w,h,s)



prefig = plt.figure(figsize=(12, 9), dpi=100, frameon=False)
#postfig = plt.figure(figsize=(9, 10), dpi=100, frameon=False)

w = 10
h = 5
s = 7

# bounds in local (not normalized Figure) units for the visible content on a given axis.  Anything outside these 
# bounds will be cropped.
x_bounds = [-1 , w + 1] 
y_bounds = [-1, (h+0.5)*2 + 1]

# our collection of generated axes objects
axs = []
axs += makeaxesgrid(prefig,2,2,2)
#axs += makeaxes(prefig, 3)

# Actually putting content into the axes is not generalizable; any given program might want to manipulate any 
# combination of axes doing different things in different ways.  So creating a set of axes and putting stuff into them
# is a per-program process (and really the intent here is for that to be pretty much the ONLY thing a given drawing
# program needs to do, with everything else library calls for generalized processes).
for a in axs:
    patches = []
    th = draw_thingy(w,h)
    for p in th:
        collection = PatchCollection(p, match_original=True)
        a.add_collection(collection)

    a.set_xlim(x_bounds)
    a.set_ylim(y_bounds)

# write this out to svgs

writefigure(prefig)
plt.show()


