from pyo import *

class ShellMode():
  """
  A set of envelopes wrapped in pyo Sig objects.
  
  """
  
  def __init__(self, num, envs=[]):
    num_list = range(num)
    self._sigs = [Sig(0) for i in num_list]
    if not envs:
      envs = [0 for i in num_list]
    self.setEnvs(envs)    
  
  # Play each envelope
  def play(self):
    for s in self._envs:
      s.play()
 
  # Update the value of each sig
  def setEnvs(self, envs):
    self._envs = envs
    for i, env in enumerate(envs):
      self._sigs[i].setValue(env)
    
  # Return the sig objects. 
  def getEnvs(self):
    return self._sigs
    
class ShellAdsr():
  def __init__(self, num=1, dur=5, dur_fact=1):
    self._dur_fact = dur_fact
    dur = dur*dur_fact
    self._envs = [Adsr(attack=dur*.05, decay=dur*.25, sustain=dur*.6, release=dur*.1, dur=dur, mul=num*.1)
      for i in range(1, num+1)]
      
  def getEnvs(self):
    return self._envs
  
  # Set the shape of the Adsr
  def setEnvsDur(self, dur):
    dur = dur*self._dur_fact
    for env in self._envs:
      env.setAttack(dur*.05)
      env.setDecay(dur*.25)
      env.setSustain(dur*.6)
      env.setRelease(dur*.1)
      env.setDur(dur)
    