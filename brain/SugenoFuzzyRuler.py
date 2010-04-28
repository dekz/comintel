def trapezoidFuzzyMembership(q,x):
    """ Trapezoidal membership function """
    a,b,c,d = q # quadruple
    if x<=a:
        return 0
    elif x<b:
        return (x-a)/(b-a)
    elif x<=c:
        return 1
    elif x<d:
        return (x-d)/(c-d)
    else:
        return 0


class SugenoFuzzyRuler:
    """
        Container for a set of fuzzy rules

        A rule is a pair (antecedents, output_constant)
        For example,
        (   
          [
            (None,'age',(2,3,5,6)) ,
            ('and','height',(0,3,3,5)) ,
            ('or', 'weight',(10,10,20,30)
          ]
          ,
          56  # Sugeno  output constant
        )
        represents the rule
        if 'age' in (2,3,5,6) and 'height' in (0,3,3,5) or 'weight' in (10,10,20,30)
        then output is 56

        Rules can be added to the container.
        The output of this collection of rules for a given input Xdic is computed
        by calling the output method with the dictionary Xdic matching variable names to
        numerical values.
    """
    
    def addRule(self,rule):
        self.rules.append(rule)

    def __init__(self, ListOfRules=None):
        if ListOfRules is None:
            ListOfRules=[]
        self.rules = ListOfRules
        self.op = {'and':lambda x,y:min(x,y) , \
                   'or':lambda x,y:max(x,y),\
                   None:lambda x,y:y} # 'None' is used for the first term  of the rule

    def output(self,Xdic,verbose=False):
        """
            Xdic is dictionary mapping input variable names to input values.
            This method computes the output of the fuzzy rule set.
            Set verbose to true to display debug information
        """
        La =[]
        Lw = []
        for rule in self.rules:
            L,out = rule
            s = 1 # current satisfaction of the rule
            for t in L:
                o,n,q = t # extract operator, name , and quadruple of the term
                x = trapezoidFuzzyMembership(q,Xdic[n])
                if verbose:
                    if o!=None:
                        print o,' ',
                    print n,'is {0:.2f} in '.format(Xdic[n]), '({0:.2f},{1:.2f},{2:.2f},{3:.2f})'.format(q[0],q[1],q[2],q[3]), " = {0:.2f}".format(x), 
                s = self.op[o](s,x)
            if verbose:
                print '  (sat,out)= ({0:.2f},{1:.2f})'.format(s,out)
            La.append(out)
            Lw.append(s)
        waSum = sum([w*a for w,a in zip(Lw,La)])  # combine the rules outputs
        sumLw = sum(Lw)
        if sumLw==0:
            if verbose:
                print 'action = 0'
            return 0
        else:
            if verbose:
                print 'action = {0:.2f}'.format(waSum/sumLw)
            return waSum/sumLw #


if  __name__ == '__main__': # do some tests
    sfr = SugenoFuzzyRuler()
    sfr.addRule( ( [ (None,'a',(0,0,2,3)) , ('and','b',(2,4,6,7) )] , 5) )
    sfr.addRule( ( [ (None,'c',(0,0,2,3)) , ('or','b',(2,4,6,7))  , ('or','a',(1,4,6,7)) ] , 4) )
    dx = {'a':1,'b':6.5 , 'c':0}
    print sfr.output(dx)
    
