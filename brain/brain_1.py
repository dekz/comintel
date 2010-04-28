
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
      self.sfr_rot.addRule( ( [ (None,'minRightSide',self.D_SMALL), ('and','minLeftSide',self.D_SMALL) , ('and','minFront',self.D_SMALL)] , 0.8) )
      self.sfr_rot.addRule( ( [ (None,'minRightSide',self.D_LARGE), ('and','minLeftSide',self.D_LARGE) , ('and','minFront',self.D_OK)] , 0.2) )
      self.sfr_rot.addRule( ( [ (None,'minRightSide',self.D_LARGE), ('and','minLeftSide',self.D_LARGE) , ('and','minFront',self.D_LARGE)] , 0.2) )
      self.sfr_trans.addRule( ( [ (None,'minRightSide',self.D_LARGE), ('and','minLeftSide',self.D_LARGE), ('and','minFront',self.D_LARGE) ] , 0.5) )
#      self.sfr_rot.addRule( ( [ (None,'minRightSide',self.D_OK), ('and','minLeftSide',self.D_OK) , ('and','minFront',self.D_LARGE)] , 0.0) )
      self.sfr_trans.addRule( ( [ (None,'minFront',self.D_LARGE)], 0.5))
      
      
   #   self.sfr_rot.addRule( ( [ (None,'minLeftSide',self.D_OK), ('and','minRightSide',self.D_LARGE)], 0.2))
    #  self.sfr_trans.addRule( ( [ (None,'minLeftSide',self.D_OK), ('and','minRightSide',self.D_LARGE)], 0.4))
    #  self.sfr_rot.addRule( ( [ (None,'minRightSide',self.D_OK), ('and','minLeftSide',self.D_LARGE)], -0.2))
    #  self.sfr_trans.addRule( ( [ (None,'minRightSide',self.D_OK), ('and','minLeftSide',self.D_LARGE)], 0.4))
      
      #FRONT
         #Too close
            #Left Corner
      self.sfr_rot.addRule( ( [ (None,'minFront',self.D_OK), ('and','minRightSide',self.D_OK)], 0.9))
      self.sfr_trans.addRule( ( [ (None,'minFront',self.D_OK), ('and','minRightSide',self.D_OK)], 0.2))
      self.sfr_rot.addRule( ( [ (None,'minFront',self.D_OK), ('and','minRightSide',self.D_SMALL)], 0.9))
      self.sfr_trans.addRule( ( [ (None,'minFront',self.D_OK), ('and','minRightSide',self.D_SMALL)], 0.2))
            #Right Corner
      self.sfr_rot.addRule( ( [ (None,'minFront',self.D_OK), ('and','minLeftSide',self.D_OK)], -0.9))
      self.sfr_trans.addRule( ( [ (None,'minFront',self.D_OK), ('and','minLeftSide',self.D_OK)], 0.2))
      self.sfr_rot.addRule( ( [ (None,'minFront',self.D_OK), ('and','minLeftSide',self.D_SMALL)], -0.9))
      self.sfr_trans.addRule( ( [ (None,'minFront',self.D_OK), ('and','minLeftSide',self.D_SMALL)], 0.2))
      
         #dead end
      self.sfr_rot.addRule( ( [ (None,'minFront',self.D_SMALL), ('and','minLeftSide',self.D_SMALL) , ('and','minRightSide',self.D_SMALL)] , 0.9) )
     # self.sfr_trans.addRule( ( [ (None,'minFront',self.D_SMALL), ('and','minLeftSide',self.D_SMALL) , ('and','minRightSide',self.D_SMALL)] , -0.4) )

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
      self.sfr_rot.addRule( ( [ (None,'s0',self.D_OK), ('and','s2',self.D_LARGE)], 0.9))
      self.sfr_trans.addRule( ( [ (None,'s0',self.D_OK), ('and','s2',self.D_LARGE)], 0.3))
      #Right | Wall ending
      self.sfr_rot.addRule( ( [ (None,'s5',self.D_LARGE), ('and','s7',self.D_OK)], -0.9))
      self.sfr_trans.addRule( ( [ (None,'s5',self.D_LARGE), ('and','s7',self.D_OK)], 0.3))
      
      
      
   def step(self):
      """
         Step function called at each iteration of the simulator.
      """
      # Gather sensor values
      self.sonar_sense()
      # create a dict of inputs for the fuzzy rules
      #dx = {'minRightSide':min(self.sv[5:10]),'minFront':min(self.sv[3:5]),'minLeftSide':min(self.sv[0:5]),\
      #      's5':self.sv[5]*1.60,'s6':self.sv[6]*1.1, 's1':self.sv[1]*1.10,'s2':self.sv[2]*1.6} # normalize sonar 5 and 6
      dx = {'minRightSide':min(self.sv[5:10]),'minFront':min(self.sv[3:5]),'minLeftSide':min(self.sv[0:4]),\
            's0':self.sv[0],'s2':self.sv[1], 's5':self.sv[6],'s7':self.sv[7]} # normalize sonar 5 and 6
      t_speed = self.sfr_trans.output(dx,False)   # to display debug information pass 'True' instead of 'False'
      r_speed = self.sfr_rot.output(dx,False)  # to display debug information pass 'True' instead of 'False'
      #print '(t_speed, r_speed) = ({0:.2f},{1:.2f})'.format(t_speed, r_speed)
      self.robot.move(t_speed, r_speed)



   def sonar_sense(self):
      """
         Compute the sonar vector self.sv, its minimum self.minDist and the index
         of minDist.
      """
      self.sv = [s.distance() for s in self.robot.range]
      #print self.sv



# ---------------- Do not change the code below (part of the framework) --------------------
def INIT(engine):
   if engine.robot.type not in ['K-Team', 'Pyrobot']:
      raise "Robot should have light sensors!"
   return FuzzySugenoBrain('roach_1', engine)
      