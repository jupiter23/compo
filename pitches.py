from pyo import *

class Tuning():
  # Generate pitch frequency values for a given root frequency for each tuning
  # Consider moving to it's own class
  def makeFreqLists(self, tuning, root=None):
    if (root==None):
      root=self._root
    
    self._freqs={
      'just' : [root, root*16/15, root*9/8, root*6/5, root*5/4, root*4/3, root*64/45, root*3/2, root*8/5, root*5/3, root*16/9, root*15/8],
      'equal_12' : [root * (2.**(i/12.))  for i in range(0, 11)],
      'equal_5' : [root * (2. **(i/5.))  for i in range(0, 4)],
      'pyth' : [root, root*1.053, root*1.125, root*1.85, root*1.265, root*1.333, root*1.404, root*1.424, root*1.5, root*1.58,
        root*1.687, root*1.778, root*1.898],
      'harmonic' : [root * i for i in range(1, 20)]
    }
  
  def just(self, root):
    return [root, root*16/15, root*9/8, root*6/5, root*5/4, root*4/3, root*64/45, root*3/2, root*8/5, root*5/3, root*16/9, root*15/8]
    
  def equal(self, root, num_tones):
    return [root * (2.**(i/float(num_tones)))  for i in range(0, num_tones - 1)]
  
  def pyth(self, root):
    return [root, root*1.053, root*1.125, root*1.85, root*1.265, root*1.333, root*1.404, root*1.424, root*1.5, root*1.58,
      root*1.687, root*1.778, root*1.898]
    
  def harmonic(self, root, num_tones):
    return [root * i for i in range(1, num_tones)]
  
  def funcsMap(self, tuning, **kwargs):
    funcs = {'just':self.just, 'equal':self.equal, 'pyth':self.pyth, 'harmonic':self.harmonic}
    return funcs[tuning]
    
  

class Pitches():
  """
  A set of pitch frequency values wrapped in Sig pyo objects.
  
  Nomenclature:
  
    Tuning:
      A tuning or a scale is a set of frequency values defined by relative positions to each other.
      Examples of tunings provided by default: 
        "equal_12": the usual 12 degree equal temperament
        "equal_5": an equal temperament of five degrees
        "pyth": the pythagorean scale
        etc. 
    
    Register:
      Not implemented yet.
      A register is a set of degrees within a range of frequencies bound within root*n and root*(n+1).
      An 'octave' in regular music nomenclature.
    
    Root:
      Root is the base frequency from which all the degrees in a tuning are calculated.
    
    Degree:
      A degree is the index of a value within a scale or tuning.  For example in the equal_12 tuning degree 7 is equivalent to the musical interval
      "fifth", and degree 0 is the root.  Upon instantiation, a Pitches object will provide a pitch for each argued degree.
  
    Position:
      The position of a given Sig object in the list of pitches for the instance. 
      
    Pitch:
      A frequency value wrapped in a Sig pyo object.  The number of pitches for a given instance is equal to the number of degrees with which the
      instance was created.
  
  :Args:
  
      root : float, optional
          Frequency in cycles per second. Defaults to 277.2.

      tuning: string
          One of the available tuning schemes
          
      degrees: list
          List of the degree positions required from the tuning scheme
          
      registers: int
          Not implemented yet
          Number of registers to calculate initially.
  """
  def __init__(self, root = 275, tuning='just', degrees=[1], registers=1):
    self._degrees = degrees
    self.len = len(degrees)
    self.setRoot(root, reset=False)
    self.setTuning(tuning)
    self.initSigs(len(degrees))
    self.setPitchesByDegree(degrees)

  # Set the Pitches root value from which to work out the various degrees according to specific tunings
  def setRoot(self, root, reset=True):
    self._root = root
    self.makeFreqLists()
    if (reset):
      # Calculate pitch values and Sig objects
      self.setPitchesByDegree(degrees=None)
      
  # Set the tuning scheme 
  def setTuning(self, tuning, reset=False):
    self._tuning = tuning
    if (reset):
      # Recalculate pitch values and Sig objects
      self.setPitchesByDegree(degrees=None)

  # Initialize a Sig object for each degree 
  def initSigs(self, num):
    self._sigs=[Sig(0) for i in range(0, num)]
    
  # Generate pitch frequency values for a given root frequency for each tuning
  # Consider moving to it's own class
  def makeFreqLists(self, root=None):
    if (root==None):
      root=self._root
    
    self._freqs={
      'just' : [root, root*16/15, root*9/8, root*6/5, root*5/4, root*4/3, root*64/45, root*3/2, root*8/5, root*5/3, root*16/9, root*15/8],
      'equal_12' : [root * (2.**(i/12.))  for i in range(0, 11)],
      'equal_5' : [root * (2. **(i/5.))  for i in range(0, 4)],
      'pyth' : [root, root*1.053, root*1.125, root*1.85, root*1.265, root*1.333, root*1.404, root*1.424, root*1.5, root*1.58,
        root*1.687, root*1.778, root*1.898],
      'harmonic' : [root * i for i in range(1, 20)]
    }

  # Set instance Pitches from scale degree
  def setPitchesByDegree(self, degrees=None, reset=True):
    if (degrees==None):
      degrees=self._degrees
    self._pitches=[self.getDegreeValue(x) for x in degrees]
    if (reset):
      self.setSigValues()

    
  # Wrap instance pitch frequencies values in Sig pyo objects
  def setSigValues(self):
    for i, sig in enumerate(self._sigs):
      sig.setValue(self._pitches[i])
      
  # Change the pitch for a Sig
  def setDegrees(self, pos, degrees):
    for i, pos in enumerate(pos):
      self._sigs[pos].setValue(self.getDegreeValue(degrees[i]))
        
  # Given a scale degree, return the frequency value.
  def getDegreeValue(self, degree):
    length = len(self._freqs[self._tuning])
    # Return the degree value
    if (degree < length):
      return self._freqs[self._tuning][degree]
    # Calculate value for degree frequency > 2*root
    else:
      return self._freqs[self._tuning][degree%length] * ((degree/length)+1)
         
  # Return all the Sig objects or the Sig objects indicated by the pos argument
  def getPitches(self, pos='all'):
    if (pos=='all'):
      return self._sigs
    return [self._sigs[i] for i in pos]
   
  # Get root freq value
  def getRoot(self):
    return self._root

  def getFreqs(self):
    return [x.value for x in self._sigs]

if __name__ == '__main__':
  s = Server().boot()
  p = Pitches(tuning='just', root=200, degrees=[0,4,7,11])
  count = 0

  def alternTuning():
    global count
    tuning='equal_12'
    if (count%2):
      tuning='equal_5'
    
    p.setTuning(tuning, reset=True)
    count+=1
    
  def changeDegree():
    global count
    degrees=[0,4,7,19]
    if (count%2):
      degrees=[0,7,12,27]
    p.setDegrees(sig_pos=[0,1,2,3], degrees=degrees)
    count+=1
  
  def changeRoot():
    if (p.getRoot() > 50):
#      factor = 0.888 #major second
#      factor = 0.9497 #minor second
#      factor = 0.66666 # fifth
      factor=0.999
      p.setRoot(p.getRoot()*factor)

  def changeBase():
    global count
    degree = 0
    if (count%2):
      degree = 7
    p.setDegrees([0], [degree])
    count += 1
      
  # Provide all the pitches to a Sine object 
  out = Mix(Sine(p.getPitches()), voices=2, mul=0.25).out()

  # Provide one of the pitches to a SuperSaw, the others to a Sine
#  ss = SuperSaw(p.getPitches([0]))
#  sine = Sine(p.getPitches([1,2,3]))
#  out = Pan(Mix([ss, sine], voices=2, mul=0.25)).out()

  pat = Pattern(alternTuning, time=0.5).play()
  s.gui(locals())