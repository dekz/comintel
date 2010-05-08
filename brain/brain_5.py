
"""

Brain for 2010 INB860 assignment 

WARNING: compass not reliable if you move the robot with the mouse
"""

from pyrobot.brain import Brain, avg

import math
import random

class Simpleton(Brain):
    
    def setup(self):
      unit_angle = "d" 
      #Initialise various variables
      self.postrack = 0,0
      self.theta = 0
      self.total_x = 0
      self.total_y = 0
      self.firstwall = 0
      
      self.compassNoiseSigma = 0.0
      self.lap_counter = 0
        
      self.safetyDistance = 0.2 # tolerated distance to wall
      self.targetDist = 0.4
      self.state_behavior_map = {'farFromWall':self.wander,\
                                 'lost':self.wander,\
                                 'inNiche': self.hide,\
                                 'almostColliding':self.emergency_turn,\
                                 'rightDistanceToWall':self.approach_obstacle,\
                                 'rightPoseToWall':self.wall_follow,\
                                 'nearWall': self.approach_obstacle,\
                                 'nearCorner': self.followCorner,\
                                 'completed.lap': self.lap_complete}
      self.state = 'lost'
      
      pass

    def step(self):
        
      self.test()      
      # Gather sensor values
      self.sonar_sense()
      # Determine current state
      self.determine_state()
      print "state = ", self.state
      t_speed,r_speed = self.state_behavior_map[self.state]()
      self.robot.move(t_speed, r_speed)
      self.pos_tracker()
      if self.total_x > 15 or self.total_y > 15:
          self.lap_counter = self.lap_counter +1
      
      



    def test(self):
      i_left,rgb_left = self.lightDetectorRead("left")
      i_right,rgb_right = self.lightDetectorRead("right")
      heading = self.compassRead()
      print i_left,rgb_left, i_right,rgb_right
      print "heading : ",heading
              
    def pos_tracker(self):

      t_speed,r_speed = self.state_behavior_map[self.state]()

      delta_th = r_speed * 12
      self.theta = self.theta + delta_th
      theta_rad = (self.theta * math.pi )/180
      
      delta_r = t_speed * math.cos(delta_th)
      
      delta_x = delta_r * math.cos(theta_rad)      
      delta_y = delta_r * math.sin(theta_rad)
      
      self.total_x = self.total_x + delta_x
      self.total_y = self.total_y + delta_y

      print "t_speed = ", t_speed
      print "r_speed = ", r_speed
      print "D change = ", self.theta
      print "X change", self.total_x
      print "Y change", self.total_y

      return

      
    def lap_complete(self):
      print "LAP COMPLETED!"
      return 0,0

    def compassRead(self): # THIS FUNCTION SHOULD NOT BE CHANGED
      """
         Return a noisy compass heading. North is zero, West is 90, South 180
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
         Compute the sonar vector self.sv, its minimum self.minDist and the index
         of minDist.
      """
      self.sv = [s.distance() for s in self.robot.range]
      self.minDist = min(self.sv)
      self.iMinDist = self.sv.index(self.minDist)
        




    def determine_state(self):
      """ PRE: self.sonar_sense() has been called """
      
      if self.lap_counter > 1:
          if (-10 < self.total_x < 10) and (-10 < self.total_y < 10):
              self.state = 'completed.lap'
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
            return 0.15, 0.15  # turn left
         if 4<self.iMinDist: # obstacle on the right
            #print "approach_obstacle:: obstacle on the right"
            return 0.15, -0.15 # turn right
         return 0.15,0
      elif self.targetDist-0.1>self.minDist: # too close
         if self.iMinDist<3: # obstacle on the left
            #print "approach_obstacle:: obstacle on the left"
            return -0.05, -0.1  # backward right
         if 4<self.iMinDist: # obstacle on the right
            #print "approach_obstacle:: obstacle on the right"
            return -0.05, 0.1 # backward left
         return -0.05,0.1
      else:
         # right distance
         if self.iMinDist==7:
            self.state = 'rightPoseToWall'
            return 0,0
         else:
            self.state = 'rightDistanceToWall'
            return 0, 0.15 # turn to make sonar 7th the smallest

            

    def wall_follow(self):
      """
         PRE state == 'rightPoseToWall' and sv[7] == minDist
         Wall follow right hand
      """
      
      if (self.firstwall == 0):
          self.theta = 0
          self.total_x = 0
          self.total_y = 0
      if self.targetDist-0.2<self.minDist<self.targetDist+0.2:
         print "forward"
         t_speed,r_speed = 0.2, 0  # cruise forward
      if self.minDist<self.targetDist-0.2:
         t_speed,r_speed = 0.2, 0.2  # correct to the left   
      if self.targetDist+0.2<self.minDist:
         t_speed,r_speed = 0.2, -0.2  # correct to the right

      self.firstwall = self.firstwall + 1   
            
                 
      return t_speed,r_speed



    def followCorner(self):
      """
         PRE state == 'nearCorner'
         Turn around the corner
      """
      if self.sv[7]>self.targetDist+0.1: # gone past the end of the wall
            print "followCorner::  spin right"
            return 0.0, -0.3  # turn right:
      if self.targetDist+0.1>self.sv[7]> self.targetDist-0.1:
         print "followCorner::  forward right"
         return 0.05, -0.15  # forward right
      if self.targetDist+0.1<self.sv[7]:
         print "followCorner:: right"
         return 0.05, -0.15 # turn right
      if self.targetDist-0.1>self.sv[7]:
         print "followCorner:: left"
         return 0.05, 0.15  # turn left
      


    def hide(self):
      """
         Behavior to hide in a niche
         This behavior uses a memory (the boolean variable self.hiding)
      """
      if min(self.sv[3:5])<2: # obstacle in front, not looking out of the niche, need to spin
         print "hide:: spin"
         return 0.0, 0.5  # turn left
      else:
         print "hide:: wait"
         return 0,0  # just keep still



    def emergency_turn(self):
      """
         Behavior to avoid collision 
      """
      
      if min(self.sv[1:7])<self.safetyDistance: # obstacle 
         print "emergency_turn:: spin"
         return -0.4, 0.0  # reverse
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
