
"""

Brain for 2010 INB860 assignment 

WARNING: compass not reliable if you move the robot with the mouse
"""

from pyrobot.brain import Brain, avg

import math
import random

class Simpleton(Brain):
   def setup(self):
      self.compassNoiseSigma = 0.05
      pass

   def step(self):
      self.test()
      t_speed,r_speed = 0.1, 0.1
      self.robot.move(t_speed, r_speed)

   def test(self):
      i_left,rgb_left = self.lightDetectorRead("left")
      i_right,rgb_right = self.lightDetectorRead("right")
      heading = self.compassRead()
      print i_left,rgb_left, i_right,rgb_right, heading
      print "compass : ",self.compassRead()



   def compassRead(self): # THIS FUNCTION SHOULD NOT BE CHANGED
      """
         Return a noisy compass heading. North is zero, West if 90, South 180
         East 270.
      """
      ignoredx,ignoredy, th = self.robot.simulation[0].getPose(self.robot.name)
      return (th+random.gauss(0,self.compassNoiseSigma))%(2*math.pi)



   def lightDetectorRead(self,side):
      """
         Side is either "left" or "right"
      """
      ls = self.robot.light[0][side][0] # light sensor on the given side 
      return ls.value, ls.rgb  # intensity and triplet of [r,g,b] values

      
   def sonar_sense(self):
      """
         Compute the sonar vector sv, its minimum minDist and the index
         of minDist.
      """
      sv = [s.distance() for s in self.robot.range]
      minDist = min(self.sv)
      iMinDist = self.sv.index(self.minDist)
      return sv, minDist, iMinDist
      


def INIT(engine):
   if engine.robot.type not in ['K-Team', 'Pyrobot']:
      raise "Robot should have light sensors!"
   return Simpleton('2010_INB860_Brain_0', engine)
      

## + + + + + + + +  CODE CEMETARY  + + + + + + + +
##
##      leftSpeed = rRight/255.0
##      rightSpeed = rLeft/255.0

##      rMean = (rLeft+rRight)*0.5;
##      leftSpeed = (rRight-rMean)/255.0 +0.1
##      rightSpeed = (rLeft-rMean)/255.0 +0.1
