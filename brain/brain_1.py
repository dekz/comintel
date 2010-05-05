
"""

Code illustrating how fuzzy elementary behaviors can be combined.


Last code update:
2010 - 04 - 02

Written for an INB860 tutorial by FM

A behavior returns a tuple (t_speed, r_speed) for following a wall on the right.

"""

from pyrobot.brain import Brain

import math
import random
from SugenoFuzzyRuler import SugenoFuzzyRuler


class FuzzySugenoBrain(Brain):
   """
      A demo brain for a pioner with a complete ring of 16 sonars.
      Demonstrate a wall following on the right behavior.
   """

   
   def setup(self):
      """
         Initialization function called by the framework
         Define the fuzzy rules
      """
      self.sfr_rot = SugenoFuzzyRuler()
      self.sfr_trans = SugenoFuzzyRuler()
      self.D_OK = (0.2,0.4,0.6,0.7) # distance ok fuzzy set
      self.D_LARGE = (0.6,0.7,100,100) # distance large fuzzy set
      self.D_SMALL = (0,0,0.1,0.3) # distance small fuzzy set
      #Rules for rotation then translation
      self.setRules()
      self.states = {'followLeft': self.followLeft,\
                     'wander': self.wander,\
                     'followRight': self.followRight}
      self.state = 'wander'
      
      
      
   def step(self):
      self.sonar_sense()
      self.getState()
      t_speed, r_speed = self.states[self.state]()
      self.robot.move(t_speed, r_speed)
     # print self.state



   def sonar_sense(self):
      self.sv = [s.distance() for s in self.robot.range]
      #print self.sv

   def getState(self):
      if ( 0.2 <= self.sv[0] <= 0.8) and ( 0.8 <= self.sv[1] <= 100) :
         #print 'wall ending on left side'
         self.state = 'followLeft'
         return
      if ( 0.2 <= self.sv[7] <= 0.8) and ( 0.8 <= self.sv[6] <= 100) :
         #print 'wall ending on right side'
         self.state = 'followRight'
         return
      if (self.state == 'followLeft') and not (0.1 <= self.sv[0] <= 0.7):
         #print 'I was following left and now my first sensor is large'
         self.state = 'followLeft'
         return
      if (self.state == 'followRight') and not (0.1 <= self.sv[7] <= 0.7):
         self.state = 'followRight'
         #print 'I was following right and now my last sensor is large'
         return

      self.state = 'wander'
      
      
   def followLeft(self):
      #print 'going left'
      return 0.4, 0.8
   
   def followRight(self):
      #print 'going right'
      return 0.4, -0.8
   
   def wander(self):
      self.sonar_sense()
      dx = {'minRightSide':min(self.sv[5:10]),'maxFront':max(self.sv[3:5]), 'minFront':min(self.sv[3:5]),'minLeftSide':min(self.sv[0:4]),'maxRightSide':max(self.sv[5:10]), 'maxLeftSide':max(self.sv[0:4]),\
            's0':self.sv[0],'s2':self.sv[1], 's5':self.sv[6],'s7':self.sv[7]}
      t_speed = self.sfr_trans.output(dx,False)   # to display debug information pass 'True' instead of 'False'
      r_speed = self.sfr_rot.output(dx,False)  # to display debug information pass 'True' instead of 'False'
      print '(t_speed, r_speed) = ({0:.2f},{1:.2f})'.format(t_speed, r_speed)
      return t_speed, r_speed

   def setRules(self):
      #self.sfr_rot.addRule( ( [ (None,'minRightSide',self.D_SMALL), ('and','minLeftSide',self.D_SMALL) , ('and','minFront',self.D_SMALL)] , 0.8) )
      #self.sfr_rot.addRule( ( [ (None,'minRightSide',self.D_LARGE), ('and','minLeftSide',self.D_LARGE) , ('and','minFront',self.D_OK)] , 0.2) )
      #self.sfr_rot.addRule( ( [ (None,'minRightSide',self.D_LARGE), ('and','minLeftSide',self.D_LARGE) , ('and','minFront',self.D_LARGE)] , 0.2) )
      #self.sfr_trans.addRule( ( [ (None,'minRightSide',self.D_LARGE), ('and','minLeftSide',self.D_LARGE), ('and','minFront',self.D_LARGE) ] , 0.5) )
      self.sfr_rot.addRule( ( [ (None,'minRightSide',self.D_LARGE), ('and','minLeftSide',self.D_LARGE) , ('and','minFront',self.D_LARGE)] , 0.2) )
      self.sfr_trans.addRule( ( [ (None,'minRightSide',self.D_LARGE), ('and','minLeftSide',self.D_LARGE), ('and','minFront',self.D_LARGE) ] , 0.5) )
      self.sfr_trans.addRule( ( [ (None,'minFront',self.D_LARGE)], 0.5))
      self.sfr_rot.addRule( ( [ (None,'minFront',self.D_LARGE)], 0.0))


      #wall in front
      self.sfr_rot.addRule(([(None, 'minFront', self.D_SMALL), ('and', 'maxRightSide', self.D_LARGE), ('and', 'maxLeftSide', self.D_LARGE)], 0.9))
      self.sfr_trans.addRule(([(None, 'minFront', self.D_SMALL), ('and', 'maxRightSide', self.D_LARGE), ('and', 'maxLeftSide', self.D_LARGE)], 0.1))
      self.sfr_rot.addRule(([(None, 'minFront', self.D_OK), ('and', 'maxRightSide', self.D_LARGE), ('and', 'maxLeftSide', self.D_LARGE)], 0.9))
      self.sfr_trans.addRule(([(None, 'minFront', self.D_OK), ('and', 'maxRightSide', self.D_LARGE), ('and', 'maxLeftSide', self.D_LARGE)], 0.1))
      #Wall on right and front
      self.sfr_rot.addRule(([(None, 'minFront', self.D_SMALL), ('and', 'maxRightSide', self.D_OK), ('and', 'maxLeftSide', self.D_LARGE)], 0.9))
      self.sfr_trans.addRule(([(None, 'minFront', self.D_SMALL), ('and', 'maxRightSide', self.D_OK), ('and', 'maxLeftSide', self.D_LARGE)], 0.1))
      self.sfr_rot.addRule(([(None, 'minFront', self.D_OK), ('and', 'maxRightSide', self.D_OK), ('and', 'maxLeftSide', self.D_LARGE)], 0.9))
      self.sfr_trans.addRule(([(None, 'minFront', self.D_OK), ('and', 'maxRightSide', self.D_OK), ('and', 'maxLeftSide', self.D_LARGE)], 0.1))
      #wall on left and front
      self.sfr_rot.addRule(([(None, 'minFront', self.D_SMALL), ('and', 'maxLeftSide', self.D_OK), ('and', 'maxRightSide', self.D_LARGE)], -0.9))
      self.sfr_trans.addRule(([(None, 'minFront', self.D_SMALL), ('and', 'maxLeftSide', self.D_OK), ('and', 'maxRightSide', self.D_LARGE)], 0.1))
      self.sfr_rot.addRule(([(None, 'minFront', self.D_OK), ('and', 'maxLeftSide', self.D_OK), ('and', 'maxRightSide', self.D_LARGE)], -0.9))
      self.sfr_trans.addRule(([(None, 'minFront', self.D_OK), ('and', 'maxLeftSide', self.D_OK), ('and', 'maxRightSide', self.D_LARGE)], 0.1))
      
      
      #Left
         #Too close
      self.sfr_rot.addRule( ( [ (None,'minLeftSide',self.D_SMALL)], -0.4))
      self.sfr_trans.addRule(( [ (None,'minLeftSide',self.D_SMALL)], 0.2))
      #Right
         #Too Close
      self.sfr_rot.addRule( ( [ (None,'minRightSide',self.D_SMALL)], 0.4))
      self.sfr_trans.addRule(([ (None,'minRightSide',self.D_SMALL)], 0.2))

      #Wall following
      #Left | Wall ending
      self.sfr_rot.addRule( ( [ (None,'s0',self.D_SMALL), ('and','s2',self.D_LARGE)], 0.99))
      self.sfr_trans.addRule( ( [ (None,'s0',self.D_SMALL), ('and','s2',self.D_LARGE)], 0.1))
      self.sfr_rot.addRule( ( [ (None,'s0',self.D_OK), ('and','s2',self.D_LARGE)], 0.99))
      self.sfr_trans.addRule( ( [ (None,'s0',self.D_OK), ('and','s2',self.D_LARGE)], 0.1))
      #Right | Wall ending
      self.sfr_rot.addRule( ( [ (None,'s5',self.D_LARGE), ('and','s7',self.D_SMALL)], -0.99))
      self.sfr_trans.addRule( ( [ (None,'s5',self.D_LARGE), ('and','s7',self.D_SMALL)], 0.1))
      self.sfr_rot.addRule( ( [ (None,'s5',self.D_LARGE), ('and','s7',self.D_OK)], -0.99))
      self.sfr_trans.addRule( ( [ (None,'s5',self.D_LARGE), ('and','s7',self.D_OK)], 0.1))

# ---------------- Do not change the code below (part of the framework) --------------------
def INIT(engine):
   if engine.robot.type not in ['K-Team', 'Pyrobot']:
      raise "Robot should have light sensors!"
   return FuzzySugenoBrain('2010_INB860_Brain_0', engine)
      