from pyo import *

class ShellManager():
  """
  Manage a set of envelopes wrapped in pyo Sig objects.

  Nomenclature:
    Shell: A set of tables used as enveloppes for sound.

    ShellManager: exposes as of enveloppes wrapped in Sig pyo objects.
  
  :Args:

    shell: A wrapper for tables to be used as enveloppes.
      For the moment only the ShellAdsr class exists.
  """
  def __init__(self, shell):
    self._sigs = [Sig(0) for i in range(shell.getNum())]
    self.setShell(shell)    
    self._shell = shell
  
  # Play each envelope or just specified envelopes
  def play(self, pos='all'):
    if (pos=='all'):
      for s in self._envs:
        s.play()
    else:
      for i in pos:
        self._envs[i].play()
 
  # Update the value of each sig
  def setShell(self, shell):
    for i, env in enumerate(shell.getEnvs()):
      self._sigs[i].setValue(env)
    self._shell = shell
    self._envs = shell.getEnvs()

  # Update the dur for each enveloppe    
  def setShellDur(self, dur):
    self._shell.setShellDur(dur)

  def getLen(self):
    return len(self._sigs)
    
  # Return the sig objects. 
  def getShell(self):
    return self._sigs

  def getShellDur(self):
    return self._shell.getDur()

class Shell():
  """
  Parent class for Shell objetcs.
  
  :Args:

    num: number of Adrs objects

    dur: Adsr dur

    dur_fact: multiplier for the Adsr dur parameter

  """
  def __init__(self, dur, num=1, dur_fact=1):
    self._num = num
    self._dur_fact = dur_fact
    dur = dur*dur_fact
    self._dur = dur

  def setShellDur(self):
    raise NotImplementedError('Shell class descendants need to implement setShellDur')  
       
  def getEnvs(self):
    return self._envs
  
  def getNum(self):
    return self._num

  def getDur(self):
    return self._dur
 
class ShellAdsr(Shell):
  """
  Wraps a number of Adsr pyo objects.
  
  :Args:

    num: number of Adrs objects

    dur: Adsr dur

    dur_fact: multiplier for the Adsr dur parameter

  """
  def __init__(self, dur, num=1, dur_fact=1):
    Shell.__init__(self, num=num, dur=dur, dur_fact=dur_fact)
    self._envs = [Adsr(attack=dur*.05, decay=dur*.25, sustain=.6, release=dur*.1, dur=dur, mul=num*.1)
      for i in range(1, num+1)]

  # Set the shape of the Adsr
  def setShellDur(self, dur):
    dur = dur*self._dur_fact
    print 'ShellAdsr dur: ', dur
    self._dur = dur
    for env in self._envs:
      env.setAttack(dur*.05)
      env.setDecay(dur*.25)
      env.setSustain(.6)
      env.setRelease(dur*.1)
      env.setDur(dur)
