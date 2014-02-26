from pyo import *

class Tuner():
  """
  Class which generates lists of frequency values according to a tuning scheme.
  """
  
  def just(self, root, *args):
    return [root, root*16/15, root*9/8, root*6/5, root*5/4, root*4/3, root*64/45, root*3/2, root*8/5, root*5/3, root*16/9, root*15/8]
    
  def equal(self, root, num_tones=12):
    return [root * (2.**(i/float(num_tones)))  for i in range(0, num_tones - 1)]
  
  def pyth(self, root, *args):
    return [root, root*1.053, root*1.125, root*1.85, root*1.265, root*1.333, root*1.404, root*1.424, root*1.5, root*1.58,
      root*1.687, root*1.778, root*1.898]
    
  def harmonic(self, root, num_tones=10):
    return [root * i for i in range(1, num_tones)]
  
  def getFreqs(self, tuning='just', root=275, num_tones=None):
    funcs = {'just':self.just, 'equal':self.equal, 'pyth':self.pyth, 'harmonic':self.harmonic}
    if num_tones is not None:
      return funcs[tuning](root, num_tones)
    return funcs[tuning](root)
  

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
      Frequency in cycles per second.  Fundamental, root pitch, lowest tone for the Pitch object.
      Defaults to 275.

    tuning: string
      One of the available tuning schemes from the Tuner class.
          
    num_tones: the number of tones for an equal temperament tuning scheme or the number of harmonics for the harmonic tuning scheme.
      Defaults to None for all other tuning schemes.
          
    degrees: list
      List of the degree positions required from the tuning scheme
          
    registers: int
      Not implemented yet
      Number of registers to calculate initially.
  """
  def __init__(self, root = 275, tuning='just', num_tones=None, degrees=[1], registers=1):
    self._degrees = degrees
    self._tuning = tuning
    self._num_tones = num_tones
    self.tuner = Tuner()
    self.len = len(degrees)
    self.setRoot(root, reset=False)
    self.initSigs(len(degrees))
    self.setPitchesByDegree(degrees)

  # Set the Pitches root value from which to work out the various degrees according to specific tunings
  def setRoot(self, root, reset=True):
    self._root = root
    self._makeFreqLists()
    if (reset):
      # Calculate pitch values and Sig objects
      self.setPitchesByDegree(degrees=None)
      
  # Set the tuning scheme 
  def setTuning(self, tuning, num_tones=None, reset=True):
    self._tuning = tuning
    self._num_tones = num_tones
    self._makeFreqLists()
    if reset:
      # Recalculate pitch values and Sig objects
      self.setPitchesByDegree(degrees=None)

  # Initialize a Sig object for each degree 
  def initSigs(self, num):
    self._sigs=[Sig(0) for i in range(0, num)]
    
  # Generate pitch frequency values for a given root frequency for each tuning
  def _makeFreqLists(self):
    self._freqs=self.tuner.getFreqs(tuning=self._tuning, root=self._root, num_tones=self._num_tones)

  # Set instance Pitches from scale degree
  def setPitchesByDegree(self, degrees=None, reset=True):
    if degrees==None:
      degrees=self._degrees
    self._pitches=[self.getDegreeValue(x) for x in degrees]
    if reset:
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
    length = len(self._freqs)
    # Return the degree value
    if (degree < length):
      return self._freqs[degree]
    # Calculate value for degree frequency > 2*root
    else:
      return self._freqs[degree%length] * ((degree/length)+1)
         
  # Return all the Sig objects or the Sig objects indicated by the pos argument
  def getPitches(self, pos='all'):
    if pos=='all':
      return self._sigs
    return [self._sigs[i] for i in pos]
   
  # Get root freq value
  def getRoot(self):
    return self._root

  # Return the frequency value for each pitch
  def getFreqs(self):
    return [x.value for x in self._sigs]

if __name__ == '__main__':
  s = Server().boot()
  p = Pitches(tuning='just', root=275, degrees=[0,4,7,10])
  count = 0

  def alternTuning():
    global count
    num_tuning_tones=12
    if (count%2):
      num_tuning_tones=5
    
    p.setTuning(tuning='equal', num_tones=num_tuning_tones, reset=True)
    count+=1
  
  # Change some positions to other tuning degrees.  
  def changeDegree():
    global count
    degrees=[0,3,5,12]
    if count%2:
      degrees=[0,5,7,13]
    p.setDegrees(pos=[0,1,2,3], degrees=degrees)
    count+=1
  
  # Change the root frequency at regular interval.
  def changeRoot():
    if p.getRoot() > 50:
#      factor = 0.888 #major second
      factor = 0.9497 #minor second
#      factor = 0.66666 # fifth
#      factor=0.999
      p.setRoot(p.getRoot()*factor)

  # Change just one tone from the list of pitches
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
