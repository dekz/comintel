
"""

Proto cockroach for INB860 tutorial


"""

from pyrobot.brain import Brain

import math
import types



class Cockroach_1(Brain):
   def setup(self):
      self.tol = 0.5 # tolerated distance to wall

   def step(self):
      #print "Starting step"
      sonar_vec = self.sonar_sense()
      #print "sonar = ", sonar_vec
      t_speed, r_speed = self.act_wander(sonar_vec)
      self.robot.move(t_speed, r_speed)

   def sonar_sense(self):
      """ return the list of current sensor values """
      return [s.distance() for s in self.robot.range]

   def act_wander(self, sv):
      left = min(sv[:3])
      front = min(sv[3:5])
      right = min(sv[5:])
      if (front < self.tol): 
         print "Obstacle in front"
         return 0, .2 # arbitrarily turn one way
      elif (right < self.tol):
         print "Obstacle right"         
         return 0, .2
      elif (left < self.tol):
         print "Obstacle left"         
         return 0, -0.2
      else:
         print "No obstacle"         
         return 0.2, 0


def INIT(engine):
   if engine.robot.type not in ['K-Team', 'Pyrobot']:
      raise "Robot should have light sensors!"
   return Cockroach_1('roach_1', engine)
      

## + + + + + + + +  CODE CEMETARY  + + + + + + + +
##
##      leftSpeed = rRight/255.0
##      rightSpeed = rLeft/255.0

##      if (left < self.tol and right < self.tol):
##         self.robot.move(0, .2)
##      elif (right < self.tol):
##         self.robot.move(0, .2)
##      elif (left < self.tol):
##         self.robot.move(0, -.2)
##      elif (front < self.tol): 
##         self.robot.move(0, .2) # arbitrarily turn one way
##      else:
##         self.robot.move(.2, 0)
