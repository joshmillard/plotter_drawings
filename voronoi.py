# voronoi stuff!

from scipy.spatial import Voronoi, voronoi_plot_2d

from cortexdraw import *

# Calculate Voronoi Polygons 
square = [(0, 0), (0, 1), (1, 1), (1, 0)]
vor = Voronoi(square)

points = []

'''
# random points
for i in range(50):
	points.append([random.random(), random.random()])
'''

'''
# trig curves, not really interesting it turns out
res = 10
for i in range(res):
	x = i/res
	y = math.sin(i/10)
	y2 = math.cos(i/10) -1
	points.append([x,y])
	points.append([x,y2])
'''


vor = Voronoi(points)

def simple_voronoi(vor, saveas=None, lim=None):
    # Make Voronoi Diagram 
    fig = voronoi_plot_2d(vor, show_points=True, show_vertices=False, s=4)

    # Configure figure 
    fig.set_size_inches(5,5)
    plt.axis("equal")

    if lim:
        plt.xlim(*lim)
        plt.ylim(*lim)

#    if not saveas is None:
#    plt.savefig("../pics/%s.png"%saveas)

    plt.show()

simple_voronoi(vor, saveas="square", lim=(-1.25,1.25))