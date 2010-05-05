#TASK3
from pyrobot.brain import Brain, avg

import math
import random

class Simpleton(Brain):
   def setup(self):
      self.compassNoiseSigma = 0.05
      self.minDistance = 0.15
      self.targetDisk = 0.4
      self.states = {'wander' :self.wander, \
                     'colliding' :self.turnAround,\
                     'searchBlue' :self.searchBlue,\
                     'deadEnd' :self.turnAround,\
                     'idle' :self.idle,\
                     'approach' :self.idle}
      self.state = 'wander'
      #pass

   def step(self):
      self.sonar_sense()
      self.lightDetectorRead()
      self.getState()
      t_speed,r_speed = self.states[self.state]
      self.robot.move(t_speed, r_speed)


   def getState(self):
      pass
   
   def turnAround(self):
      pass
   
   def searchBlue(self):
      pass
   
   def idle(self):
      pass
   
   def wander(self):
      pass




   def compassRead(self): # THIS FUNCTION SHOULD NOT BE CHANGED
      ignoredx,ignoredy, th = self.robot.simulation[0].getPose(self.robot.name)
      return (th+random.gauss(0,self.compassNoiseSigma))%(2*math.pi)



   def lightDetectorRead(self,side):
      ls = self.robot.light[0][side][0] # light sensor on the given side 
      return ls.value, ls.rgb  # intensity and triplet of [r,g,b] values

      
   def sonar_sense(self):
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
