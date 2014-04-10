from pyo import *
# test
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
      # This calls ShellMode.play(pos=[i])
      self.callers[i] = CallAfter(self._inst.play, self._lapse * i, [[i]])

class Bender():
  """
  Bend the frequency value of a pitches object.

  Each frequency value from the inst object in the pos list will be 'bent' to the frequency value of the
  same index in the target_freq list, over a time period set by the element of the same index in the dur list.
  If one of the lists is shorter, Bender will loop over the list to generate values.
  For example, if pos is [0,1,2], target_freq is [1000, 2000] and dur is [1], frequencies at pos 0 and 2 will 
  be bent to 1000 hz while frequency at pos 1 will be bent to 2000.  The bends will reach their target values
  in 1 second.  If go_back is set to true, each frequency will return to it's original value in the length of
  time defined by the appropriate position in the go_back_dur list. 

  :Args:
    inst: an instance of a pitches object
    
    pos: a list of pitches pos on which to apply the bend
    
    target_freq: a list of freq values to which the pitches will be changed
    
    dur: a list of durations to attain the target freq
    
    seg_type: 'lin' or 'exp', to use either a Linseg or Expseg object for the bend
    
    go_back: a boolean indicating if the freq(s) should go back to the original value(s) after the move
    
    go_back_dur: a list of durations to take the freqs back to the original values
  """
  def __init__(self, inst, pos, target_freq, dur, seg_type='lin', go_back=False, go_back_dur=[0]):
    self.setBend(inst, pos, target_freq, dur, seg_type, go_back, go_back_dur)
  
  def setBend(self, inst, pos, target_freq, dur, seg_type, go_back=False, go_back_dur=[0]):
    self._seg_type = Linseg if seg_type == 'lin' else Expseg 
    self._inst = inst
    self._pos = pos
    self._target_freq = target_freq
    self._dur = dur
    self._go_back = go_back
    self._go_back_dur = go_back_dur
    self._orig_freqs = None
    self._pitches = inst.getPitches(pos)
    self._bends = [None for x in pos]
    self._orig_freqs = inst.getFreqs()

    # Bring the frequency back to it's original value
    if (go_back):
      for i, pos_i in enumerate(pos):
        orig = self._orig_freqs[pos_i]
        # Create Linseg or Expseg depending on the value of the seg_type parameter
        self._bends[i] = self._seg_type([
          (0,0),
          (dur[i%len(dur)], target_freq[i%len(target_freq)] - orig),
          (dur[i%len(dur)] + go_back_dur[i%len(go_back_dur)], 0)
        ])

    # Remain at the new pitch value
    else:
      for i, pos_i in enumerate(pos):
        orig = self._orig_freqs[pos_i]
        self._bends[i] = Linseg([
          (0,0),
          (dur[i%len(dur)], target_freq[i%len(target_freq)] - orig),
        ])
  
    # Add the segments to the Sig values      
    for i, pitch in enumerate(self._pitches):
      pitch.setValue(pitch.value + self._bends[i])  
 
  # Remove the seg objects from the pitches and clear the objects from memory.
  # @TODO this method has not been tested yet
  def unsetBend(self, mode='restore'):
    for i, pos in enumerate(self._pos):
      if mode == 'restore':
        self._pitches[pos].setValue(self._orig_freqs[pos])
      else:
        # Keep the pitches to their current value.
        self._pitches[pos].setValue(self._pitches[pos].value)
      self._bends[i] = None
      
  # Read each 
  def bend(self):
    for bend in self._bends:
      bend.play()
