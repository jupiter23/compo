from pyo import *

class Strummer():
  """
  :Args:

    inst: @DEBUG an instance of ShellMode
 
  """
  def __init__(self, inst, lapse=0.1):
    self._len = inst.getLen()
    self._inst = inst
    self._lapse = lapse
    # List in which to store instances of CallAfter objects
    self.callers = [i for i in range(0, self._len)]
    
  def setInst(self, inst):
    self._inst = inst
 
  # Set the lapse of time between each enveloppe read 
  def setLapse(self, lapse):
    self._lapse = lapse
  
  def clear(self):
    for i in range(0, self._len):
      self.callers[i] = None
  
  # Read each enveloppe, one at a time
  def strum(self):
    for i in range(0, self._len):
      # @DEBUG this calls ShellMode.play(pos=[i])
      self.callers[i] = CallAfter(self._inst.play, self._lapse * i, [[i]])

class Bender():
  
