
"""

Brain for 2010 INB860 assignment 

WARNING: compass not reliable if you move the robot with the mouse
"""

from pyrobot.brain import Brain, avg
from time import *

import math
import random

class Simpleton(Brain):
    
    def setup(self):
      self.compassNoiseSigma = 0.05
      self.missionComplete = 0
      self.safetyDistance = 0.15 # tolerated distance to wall
      self.targetDist = 0.4
      self.ignoreLight = 0
      self.lightFound = 0
      self.initRotation = 0
      self.state_behavior_map = {'farFromWall':self.wander,\
                                 'lost':self.wander,\
                                 'inNiche': self.hide,\
                                 'almostColliding':self.emergency_turn,\
                                 'rightDistanceToWall':self.approach_obstacle,\
                                 'rightPoseToWall':self.wall_follow,\
                                 'nearWall': self.approach_obstacle,\
                                 'nearCorner': self.followCorner,\
                                 'chaseBlueLight':self.chaseBlueLight,\
                                 'goToLight':self.goToLight,\
                                 'rotateSearch':self.rotateSearch,\
                                 'idle':self.idle}
      self.state = 'lost'
      
      pass

    def step(self):

      self.sonar_sense()
      self.determine_state()
      t_speed,r_speed = self.state_behavior_map[self.state]()
      self.robot.move(t_speed, r_speed)

    def idle(self):
        return 0.0, 0.0
    
    def goToLight(self):
       self.lightFound = 1;
       self.initRotation = round(self.compassRead(), 1)-0.3
       i_left,rgb_left = self.lightDetectorRead("left")
       i_right,rgb_right = self.lightDetectorRead("right")
       print "Set up the rotating... Done"
    
    
    
    def chaseBlueLight(self):
      #print "Chasing Blue Light"  
      i_left,rgb_left = self.lightDetectorRead("left")
      i_right,rgb_right = self.lightDetectorRead("right")
      
      BlueLightUpper=rgb_left[2]+1
      BlueLightLower=rgb_left[2]-1
      if rgb_left[2] > 254 and rgb_right[2] > 254:
          #print "found blue light"
          self.goToLight()
          return 0, 0 #at light, wait
      if rgb_left[2] > rgb_right[2]:
         # print "Light Left"
          return 0.1, 0.2 #turn left, into light
      if rgb_right[2] > rgb_left[2]:
         # print "Light Right"
          return 0.1, -0.2 #turn right, into light
      if BlueLightUpper > rgb_left[2] > BlueLightLower:
         # print "Light Straight"
          return 0.4, 0
      
          
    def rotateSearch(self):
       i_left,rgb_left = self.lightDetectorRead("left")
       i_right,rgb_right = self.lightDetectorRead("right")
       heading = round(self.compassRead(), 1)
       if (rgb_left[2] == rgb_right[2] == 0):
           #we aren't in a room with more than one light detected
           print "Only one light detected, cool down started"
           self.lightFound = 0
           self.ignoreLight = 300
           return 0.0, 0.0
       if (heading == self.initRotation):
          #rotation complete and always lit, must be in a room with 2
          print "Found Room with 2 Lights"
          self.missionComplete = 1
          self.lightFound = 0
          self.ignoreLight = 300
          print heading, self.initRotation, (rgb_left[2] == rgb_right[2] == 0)
          return 0.0, 0.0
       else:
          print heading, self.initRotation, (rgb_left[2] == rgb_right[2] == 0)
          return 0.0, 0.1
          
    def determine_state(self):
      """ PRE: self.sonar_sense() has been called """
      
      i_left,rgb_left = self.lightDetectorRead("left")
      i_right,rgb_right = self.lightDetectorRead("right")
      if (self.ignoreLight > 0):
         self.ignoreLight -= 1
         
      if (self.missionComplete > 0):
          self.state = 'idle'
          return
          
      if (self.lightFound > 0):
         self.state = 'rotateSearch'
         return
      if (rgb_left[2]>0 or rgb_right[2]>0) and (rgb_right[1] < 1) and (rgb_left[1] < 1 and self.ignoreLight < 1):
          self.state = 'chaseBlueLight'
          return
                  
      if self.state=='inNiche':
         return # 'inNiche'  absorbing state
      if max(self.sv) < 1:
         self.state='inNiche'
         return
      if self.state=='nearCorner':
         if (self.targetDist-0.15<self.sv[7]<self.targetDist+0.15)\
            and (self.sv[7]<self.sv[6]<1.2*self.sv[7]):
            self.state = 'rightPoseToWall'
         return # 'nearCorner'  memory state
      if 4<self.minDist:
         self.state = 'farFromWall'
         return
      if self.minDist<self.safetyDistance:
         self.state =  'almostColliding'
         return
      if self.state=='rightPoseToWall' and self.sv[6]>2*self.sv[7]:
         self.state = 'nearCorner'
         return
      if self.targetDist-0.15<self.minDist<self.targetDist+0.15:
         if self.iMinDist==7:
            self.state = 'rightPoseToWall'
            return
      
      else:
            self.state =  'rightDistanceToWall'
            return
      self.state =  'nearWall'



    def approach_obstacle(self):
      """
         Go toward the closest obstacle when an obstacle detected
         within 4m. Get the robot closer to the right distance, and
         then to the right pose wrt the wall
      """
      if self.targetDist+0.1<self.minDist: # too far
         if self.iMinDist<3: # obstacle on the left
            #print "approach_obstacle:: obstacle on the left"
            return 0.3, 0.3  # turn left
         if 4<self.iMinDist: # obstacle on the right
            #print "approach_obstacle:: obstacle on the right"
            return 0.3, -0.3 # turn right
         return 0.3,0
      elif self.targetDist-0.1>self.minDist: # too close
         if self.iMinDist<3: # obstacle on the left
            #print "approach_obstacle:: obstacle on the left"
            return -0.1, -0.1  # backward right
         if 4<self.iMinDist: # obstacle on the right
            #print "approach_obstacle:: obstacle on the right"
            return -0.1, 0.1 # backward left
         return -0.1,0
      else:
         # right distance
         if self.iMinDist==7:
            self.state = 'rightPoseToWall'
            return 0,0
         else:
            self.state = 'rightDistanceToWall'
            return 0, 0.3 # turn to make sonar 7th the smallest

            

    def wall_follow(self):
      """
         PRE state == 'rightPoseToWall' and sv[7] == minDist
         Wall follow right hand
      """
      if self.targetDist-0.2<self.minDist<self.targetDist+0.2:
         #print "forward"
         return 0.2, 0  # cruise forward
      if self.minDist<self.targetDist-0.2:
         return 0.2, 0.2  # correct to the left   
      if self.targetDist+0.2<self.minDist:
         return 0.2, -0.2  # correct to the right



    def followCorner(self):
      """
         PRE state == 'nearCorner'
         Turn around the corner
      """
      if self.sv[7]>self.targetDist+0.1: # gone past the end of the wall
            #print "followCorner::  spin right"
            return 0.0, -0.1  # turn right:
      if self.targetDist+0.1>self.sv[7]> self.targetDist-0.1:
        # print "followCorner::  forward right"
         return 0.1, -0.05  # forward right
      if self.targetDist+0.1<self.sv[7]:
        # print "followCorner:: right"
         return 0.1, -0.1  # turn right
      if self.targetDist-0.1>self.sv[7]:
        # print "followCorner:: left"
         return 0.1, 0.1  # turn left
      


    def hide(self):
      """
         Behavior to hide in a niche
         This behavior uses a memory (the boolean variable self.hiding)
      """
      if min(self.sv[3:5])<2: # obstacle in front, not looking out of the niche, need to spin
       #  print "hide:: spin"
         return 0.0, 0.5  # turn left
      else:
       #  print "hide:: wait"
         return 0,0  # just keep still



    def emergency_turn(self):
      """
         Behavior to avoid collision 
      """
      if min(self.sv[1:7])<self.safetyDistance: # obstacle 
        # print "emergency_turn:: spin"
         return -0.2, 0.0  # reverse
      else: # behavior not active
         return 0, 0.1


    def wander(self, sv):
      """ Wandering behavior """
      left = min(sv[:3])
      front = min(sv[3:5])
      right = min(sv[5:])
      if (front < self.safetyDistance): 
         #print "wander:: Obstacle in front"
         return 0, .2 # arbitrarily wander
      elif (right < self.safetyDistance):
         #print "wander:: Obstacle right"         
         return 0, .2
      elif (left < self.safetyDistance):
         #print "wander:: Obstacle left"         
         return 0, -0.2
      else:
         #print "wander:: No obstacle"         
         return 0.2, random.uniform(-1,1)
    
    def compassRead(self): # THIS FUNCTION SHOULD NOT BE CHANGED
      ignoredx,ignoredy, th = self.robot.simulation[0].getPose(self.robot.name)
      return (th+random.gauss(0,self.compassNoiseSigma))%(2*math.pi)



    def lightDetectorRead(self,side):
      ls = self.robot.light[0][side][0] # light sensor on the given side 
      return ls.value, ls.rgb  # intensity and triplet of [r,g,b] values



    def sonar_sense(self):
      self.sv = [s.distance() for s in self.robot.range]
      self.minDist = min(self.sv)
      self.iMinDist = self.sv.index(self.minDist)

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
