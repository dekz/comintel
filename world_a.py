"""

A PyrobotSimulator world.
"""

from pyrobot.simulators.pysim import *

def INIT():
    # (width, height), (offset x, offset y), scale:
    sim = TkSimulator((1000,800), (0,800), 50)  
    #sim = TkSimulator((446,491),(21,451),80.517190)

    # x1, y1, x2, y2 in meters:

    # The sandbox
    sim.addBox(0.1, 0.1,19.9,15.9,"white", "brown") # inside color , wall color

    wallThickeness = 0.1
    walls=[(1.5,3.5,4,3.5),(4,3.5,4,1.5),(7.5,0,7.5,3),(15,1.5,15,2.5),\
           (15,2.5,17.5,2.5),(17.5,2.5,17.5,9),(18,11.5,20,11.5),(18,11.5,18,14.5),\
           (4,5.5,6,5.5),(4,5.5,4,9),(4,9,5,9),(6.5,9,7.5,9),(7.5,9,7.5,6),\
           (17.5,9,18.5,9),(19,6,20,6),(17.5,4,20,4),(2,11,3,11),(2,11,2,14),(2,14,7,14),(7,14,7,11),\
           (7,11,5,11),(10,4,10,14),(10,4,15,4),(10,14,15,14),(15,14,15,13),(10,11,15,11),(15,11,15,9),\
           (13,9,13,7),(13,7,15,7),(15,7,15,4),(0,6,1,6),(13,0,13,2),(8.5,16,8.5,15)]
    for wall in walls:
        x1, y1, x2, y2 = wall
        x1,x2 = min(x1,x2)-wallThickeness, max(x1,x2)+wallThickeness
        y1,y2 = min(y1,y2)-wallThickeness, max(y1,y2)+wallThickeness
        sim.addBox(x1, y1, x2, y2,"purple","brown")


    # (x, y) meters, brightness usually 1 (1 meter radius):
    sim.addLight(6, 12, 0.1, "blue")
    sim.addLight(3, 13, 0.1, "blue")
    
    sim.addLight(12, 0.5, 0.1, "yellow")
    sim.addLight(14, 5, 0.1, "red")

    sim.addLight(12, 13, 0.1, "blue")
    sim.addLight(1, 1, 0.1, "blue")
 
    # port, name, x, y, th, bounding Xs, bounding Ys, color
    # (optional TK color name):
    sim.addRobot(60000, TkPioneer("RedPioneer",
                                  3, 0.5, 0.00,
                                  ((.225, .225, -.225, -.225),
                                   (.175, -.175, -.175, .175))))
    # add some sensors:
    sim.robots[0].addDevice(PioneerFrontSonars())
    sim.robots[0].addDevice(PioneerFrontLightSensors())
    return sim



##   # (x, y) meters, brightness usually 1 (1 meter radius):
##    sim.addLight(1, 2, 0.1, "green")
##
##    # (x, y) meters, brightness usually 1 (1 meter radius):
##    sim.addLight(4, 1, 0.1, "green")
##
##    # (x, y) meters, brightness usually 1 (1 meter radius):
##    sim.addLight(2, 4, 0.1, "green")

