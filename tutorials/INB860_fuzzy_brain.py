
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


# A simple fuzzy rule system written for INB860
# send comments to f.maire@qut.edu.au
# Last modified 2010-04-02 at 10am
#




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
      # wall dist ok and no obstacle =>  go fast
      self.sfr_rot.addRule( ( [ (None,'minRightSide',self.D_OK), ('and','s6',self.D_OK) , ('and','minFront',self.D_LARGE)] , 0.0) )
      self.sfr_trans.addRule( ( [ (None,'minRightSide',self.D_OK), ('and','s6',self.D_OK), ('and','minFront',self.D_LARGE) ] , 1) )
      # too close to wall  => turn left
      self.sfr_rot.addRule( ( [ (None,'minRightSide',self.D_SMALL) ] , 0.3) )
      self.sfr_trans.addRule( ( [ (None,'minRightSide',self.D_SMALL) ] , 0.3) )
      # too far => turn right
      self.sfr_rot.addRule( ( [ (None,'minRightSide',self.D_LARGE) ] , -0.3) )
      self.sfr_trans.addRule( ( [ (None,'minRightSide',self.D_LARGE) ] , 0.3) )
      # obstacle => turn left
      self.sfr_rot.addRule( ( [ (None,'minFront',self.D_SMALL) ] , 1) )
      self.sfr_trans.addRule( ( [ (None,'minFront',self.D_SMALL) ] , 0.05) )
      self.sfr_rot.addRule( ( [ (None,'minFront',self.D_OK) ] , 0.8) )
      self.sfr_trans.addRule( ( [ (None,'minFront',self.D_OK) ] , 0.1) )
      # s5 large and s6 ok => turn a bit right
      self.sfr_rot.addRule( ( [ (None,'s5',self.D_LARGE), ('and','s6',self.D_OK) ] , -0.2) )
      self.sfr_trans.addRule( ( [ (None,'s5',self.D_LARGE), ('and','s6',self.D_OK) ] , 0.2) )
      # s5 large and s6 ok => turn a bit right
      self.sfr_rot.addRule( ( [ (None,'s5',self.D_LARGE), ('and','s6',self.D_LARGE) ] , -0.9) )
      self.sfr_trans.addRule( ( [ (None,'s5',self.D_LARGE), ('and','s6',self.D_LARGE) ] , 0.1) )
      
          

   def step(self):
      """
         Step function called at each iteration of the simulator.
      """
      # Gather sensor values
      self.sonar_sense()
      # create a dict of inputs for the fuzzy rules
      dx = {'minRightSide':min(self.sv[5:10]),'minFront':min(self.sv[3:5]),\
            's5':self.sv[5]*1.60,'s6':self.sv[6]*1.10} # normalize sonar 5 and 6
      t_speed = self.sfr_trans.output(dx,False)   # to display debug information pass 'True' instead of 'False'
      r_speed = self.sfr_rot.output(dx,False)  # to display debug information pass 'True' instead of 'False'
      print '(t_speed, r_speed) = ({0:.2f},{1:.2f})'.format(t_speed, r_speed)
      self.robot.move(t_speed, r_speed)



   def sonar_sense(self):
      """
         Compute the sonar vector self.sv, its minimum self.minDist and the index
         of minDist.
      """
      self.sv = [s.distance() for s in self.robot.range]



# ---------------- Do not change the code below (part of the framework) --------------------
def INIT(engine):
   if engine.robot.type not in ['K-Team', 'Pyrobot']:
      raise "Robot should have light sensors!"
   return FuzzySugenoBrain('roach_1', engine)
      




## + + + + + + + +  CODE CEMETARY  + + + + + + + +




##      self.sfr_rot = SugenoFuzzyRuler()
##      self.sfr_trans = SugenoFuzzyRuler()
##      self.OK_7_8 = (0.2,0.4,0.6,0.7)
##      self.LARGE_7_8 = (0.6,0.7,100,100)
##      self.SMALL_7_8 = (0,0,0.1,0.3)
##      self.LARGE_6_9 = (1.5,2,100,100)
##      self.OK_ratio_6_9 = (0.8,0.9,1.1,1.2)
##      self.SMALL_ratio_6_9 = (0,0.8,0.9,1)
##      self.LARGE_ratio_6_9 = (1,1.1,100,100)
##      # everything ok => go fast
##      self.sfr_rot.addRule( ( [ (None,'min_7_8',self.OK_7_8) , ('and','ratio_6_9',self.OK_ratio_6_9 )] , 0.0) )
##      self.sfr_trans.addRule( ( [ (None,'min_7_8',self.OK_7_8) , ('and','ratio_6_9',self.OK_ratio_6_9 )] , 1) )
##      # dist ok and ratio small => correct left
##      self.sfr_rot.addRule( ( [ (None,'min_7_8',self.OK_7_8) , ('and','ratio_6_9',self.SMALL_ratio_6_9 )] , 0.2) )
##      self.sfr_trans.addRule( ( [ (None,'min_7_8',self.OK_7_8) , ('and','ratio_6_9',self.SMALL_ratio_6_9 )] , 0.5) )
##      # dist ok and ratio large => correct right
##      self.sfr_rot.addRule( ( [ (None,'min_7_8',self.OK_7_8) , ('and','ratio_6_9',self.LARGE_ratio_6_9 )] , -0.2) )
##      self.sfr_trans.addRule( ( [ (None,'min_7_8',self.OK_7_8) , ('and','ratio_6_9',self.LARGE_ratio_6_9 )] , 0.5) )
##      # too close => turn left
##      self.sfr_rot.addRule( ( [ (None,'min_7_8',self.SMALL_7_8) ] , 0.3) )
##      self.sfr_trans.addRule( ( [ (None,'min_7_8',self.SMALL_7_8) ] , 0.3) )
##      # too far => turn right
##      self.sfr_rot.addRule( ( [ (None,'min_7_8',self.LARGE_7_8) ] , -0.3) )
##      self.sfr_trans.addRule( ( [ (None,'min_7_8',self.LARGE_7_8) ] , 0.3) )
##      # min_7_8 is OK but tip of the wall
##      self.sfr_rot.addRule( ( [ (None,'min_7_8',self.OK_7_8) , ('and','min_6_9',self.LARGE_6_9 )] , -0.5) )
##      self.sfr_trans.addRule( ( [ (None,'min_7_8',self.OK_7_8) , ('and','min_6_9',self.LARGE_6_9 )] , 0.5) )
