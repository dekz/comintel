"""
A PyrobotSimulator world. A room with one obstacle and
a small inner room.

(c) 2005, PyroRobotics.org. Licensed under the GNU GPL.
"""

from pyrobot.simulators.pysim import *

def INIT():
    # (width, height), (offset x, offset y), scale:
    sim = TkSimulator((1000,800), (0,800), 100)  
    #sim = TkSimulator((446,491),(21,451),80.517190)

    # x1, y1, x2, y2 in meters:

    # The sandbox
    sim.addBox(0.1, 0.1,9.9,7.9,"white", "brown") # inside color , wall color

    sim.addBox(1.5, 1.5, 1.8, 5.5,"brown","brown")
    sim.addBox(1.5, 5.5, 3.5, 5.3,"brown","brown")
    sim.addBox(3.5, 5.3, 3.7, 4.0,"brown","brown")   
    sim.addBox(5, 5, 5.2, 6.5,"brown","brown")
    sim.addBox(3, 1, 3.2, 2,"brown","brown")
    sim.addBox(3, 1, 10, 1.2,"brown","brown")
    sim.addBox(5.5, 2, 7, 3.5,"brown","brown")

    sim.addBox(8, 5, 8.1, 8,"brown","brown")
    sim.addBox(8.5, 3, 10, 3.2,"brown","brown")

    # (x, y) meters, brightness usually 1 (1 meter radius):
    sim.addLight(9.5, 7.5, 0.1, "yellow")
 
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

