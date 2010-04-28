
"""

Code illustrating how elementary behaviors can be combined.
In this example, we use a finite state machine to
make transition between states.

Last code update:
2010 - 03 - 22 
Written for an INB860 tutorial by FM

A behavior returns a tuple (t_speed, r_speed)

"""

from pyrobot.brain import Brain

import math
import random

class ReactiveBrain(Brain):
   """
   Simple reactive brain. Robot determines its state,
   and call the corresponding behavior. No fusion of behaviors
   is used, th winner takes all.
   To add a behavior, edit 'self.state_behave_dict' and the find state function
   """

   
   def setup(self):
      """
         Initialization function called by the framework
      """
      self.safetyDistance = 0.15 # tolerated distance to wall
      self.targetDist = 0.4
      self.state_behavior_map = {'farFromWall':self.wander,\
                                 'lost':self.wander,\
                                 'inNiche': self.hide,\
                                 'almostColliding':self.emergency_turn,\
                                 'rightDistanceToWall':self.approach_obstacle,\
                                 'rightPoseToWall':self.wall_follow,\
                                 'nearWall': self.approach_obstacle,\
                                 'nearCorner': self.followCorner}
      self.state = 'lost'

      

   def step(self):
      """
         Step function called at each iteration of the simulator.
      """
      # Gather sensor values
      self.sonar_sense()
      # Determine current state
      self.determine_state()
      print "state = ", self.state
      t_speed,r_speed = self.state_behavior_map[self.state]()
      self.robot.move(t_speed, r_speed)



   def sonar_sense(self):
      """
         Compute the sonar vector self.sv, its minimum self.minDist and the index
         of minDist.
      """
      self.sv = [s.distance() for s in self.robot.range]
      self.minDist = min(self.sv)
      self.iMinDist = self.sv.index(self.minDist)



   def determine_state(self):
      """ PRE: self.sonar_sense() has been called """
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
            return 0, 0.1 # turn to make sonar 7th the smallest

            

   def wall_follow(self):
      """
         PRE state == 'rightPoseToWall' and sv[7] == minDist
         Wall follow right hand
      """
      if self.targetDist-0.1<self.minDist<self.targetDist+0.1:
         return 0.2, 0  # cruise forward
      if self.minDist<self.targetDist-0.1:
         return 0.1, 0.1  # correct to the left   
      if self.targetDist+0.1<self.minDist:
         return 0.1, -0.1  # correct to the right



   def followCorner(self):
      """
         PRE state == 'nearCorner'
         Turn around the corner
      """
      if self.sv[7]>self.targetDist+0.1: # gone past the end of the wall
            print "followCorner::  spin right"
            return 0.0, -0.1  # turn right:
      if self.targetDist+0.1>self.sv[7]> self.targetDist-0.1:
         print "followCorner::  forward right"
         return 0.1, -0.05  # forward right
      if self.targetDist+0.1<self.sv[7]:
         print "followCorner:: right"
         return 0.1, -0.1  # turn right
      if self.targetDist-0.1>self.sv[7]:
         print "followCorner:: left"
         return 0.1, 0.1  # turn left
      

   
   def hide(self):
      """
         Behavior to hide in a niche
         This behavior uses a memory (the boolean variable self.hiding)
      """
      if min(self.sv[3:5])<2: # obstacle in front, not looking out of the niche, need to spin
         print "hide:: spin"
         return 0.0, 0.2  # turn left
      else:
         print "hide:: wait"
         return 0,0  # just keep still



   def emergency_turn(self):
      """
         Behavior to avoid collision 
      """
      if min(self.sv[1:7])<self.safetyDistance: # obstacle 
         print "emergency_turn:: spin"
         return -0.1, 0.0  # reverse
      else: # behavior not active
         return 0, 0.1


   def wander(self, sv):
      """ Wandering behavior """
      left = min(sv[:3])
      front = min(sv[3:5])
      right = min(sv[5:])
      if (front < self.safetyDistance): 
         #print "wander:: Obstacle in front"
         return 0, .2 # arbitrarily turn one way
      elif (right < self.safetyDistance):
         #print "wander:: Obstacle right"         
         return 0, .2
      elif (left < self.safetyDistance):
         #print "wander:: Obstacle left"         
         return 0, -0.2
      else:
         #print "wander:: No obstacle"         
         return 0.2, random.uniform(-1,1)


# ---------------- Do not change the code below (part of the framework) --------------------
def INIT(engine):
   if engine.robot.type not in ['K-Team', 'Pyrobot']:
      raise "Robot should have light sensors!"
   return ReactiveBrain('roach_1', engine)
      




## + + + + + + + +  CODE CEMETARY  + + + + + + + +

##   def find_state(self, sv):
##      if self.state== 'inNiche':
##         return 'inNiche'
##      if min(sv) > 4: # MAGIC NUMBER
##         return 'outback'
##      if max(sv) < 1:
##         return 'inNiche'    
##      if min(sv) < 1:
##         return 'nearObstacle'
##      return 'unknown' # some default state
##
         
      # no obstacle in front
##      # Make sure orientation is roughly parallel to the wall      
##      # ratio sv[5]/sv[7] should be in target range [1.90,2.10]
##      if sv[5]/sv[7] < 1.90:
##         print "wall_follow::  turn left to correct s5/s7 ratio"
##         return 0.1, 0.2  # turn left
##      if sv[5]/sv[7] > 2.10:         
##         print "wall_follow:: turn right to correct s5/s7 ratio"
##         return 0.1, -0.2 # turn right
      # Make sure distance to the wall is in the target range
##      minRightDist = min(sv[5:])
##      if minRightDist<0.2: # too close to the wall
##         print "wall_follow:: too close to wall"
##         return 0.1, 0.3 # turn left
##      if minRightDist>0.3: # too far from the wall
##         print "wall_follow:: too far from wall"
##         return 0.1, -0.3 # turn right
