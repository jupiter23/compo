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
  
  # Play each envelope or just specified envelopes
  def play(self, pos='all'):
    if (pos=='all'):
      for t in self._trigs:
        t.play()
    else:
      for i in pos:
        self._trigs[i].play()
 
  # Update the value of each sig
  def setShell(self, shell):
    for i, env in enumerate(shell.getEnvs()):
      self._sigs[i].setValue(env)
    self._shell = shell
    self._envs = shell.getEnvs()
    self._trigs = shell.getTrigs()

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
    self._dur = dur*dur_fact

  def setShellDur(self, dur):
    raise NotImplementedError('Shell class descendants need to implement setShellDur')  
       
  def getEnvs(self):
    return self._envs
    
  def getTrigs(self):
    return self._trigs  
    
  def getNum(self):
    return self._num

  def getDur(self):
    return self._dur

class EnvWrap():
  """
  Provides an envelope player wrapper.  Used by instruments that provide their own envelopes.
  :Args:
    wrapped: List of Pyo tables that need to be red on a Trig.
  """
  def __init__(self, wrapped):
    self._wrapped = wrapped
    self._trigs = [Trig() for x in range(0, len(self._wrapped))]
    for i, wrap in enumerate(self._wrapped):
      wrap.setInput(self._trigs[i])     
    
  def play(self, pos='all'):
    if pos == 'all':
      for t in self._trigs:
        t.play()
    else:
      for i in pos:
        self._envs[i].play()

class ShellHann(Shell):
  """
  Provide a number of Hann tables to be read as sound envelopes.
  
  :Args:
    dur: time duration for table reading by TrigEnv
    num: number of Tables to generate
    dur_fact: multiplier for the dur parameter
    items_dur_fact: individual dur multiplier for each envoloppe reader
    items_start_del: Listdelay on reading of each table reader
    mul: List of amplitude control factor for each envelope.  If not provided mul will be calculated to 1/num
  """
  def __init__(self, dur, num=1, dur_fact=1, items_dur_fact=[], items_start_del=[], mul=[]):
    Shell.__init__(self, num=num, dur=dur, dur_fact=dur_fact)
    self._num_list = range(0, num)
    if not mul:
      self._mul = [1./num for x in self._num_list]
    else:
      self._mul = [0 for x in self._num_list]
      for i, mul_i in enumerate(mul):
        self._mul[i] = mul[i%len(mul)]      
        
    self._tables = [HannTable() for x in self._num_list]
    self._trigs = [Trig() for x in self._num_list]
    self._envs = [TrigEnv(self._trigs[i], table=self._tables[i], mul=self._mul[i]) for i in self._num_list]
    self.setShellDur(dur, dur_fact, items_dur_fact)
 
  # Repetitive calls do this method that don't want to change one of the parameters should pass None.
  def setDurValues(self, dur=None, dur_fact=None, items_dur_fact=None):
    if dur != None:
      self._dur_orig = dur
    if dur_fact != None:
      self._dur_fact = dur_fact
    if items_dur_fact != None:
      self._items_dur_fact = items_dur_fact

    dur = self._dur_orig * self._dur_fact

    # Each envelope has the same dur
    if not items_dur_fact:
      self._dur = [dur for i in self._num_list]
    # Apply a factor specific to each envelope
    else:
      self._dur = [i for i in self._num_list]
      for i, item in enumerate(items_dur_fact):
        self._dur[i] = dur * items_dur_fact[i%len(items_dur_fact)]
    
  def setShellDur(self, dur=None, dur_fact=None, items_dur_fact=None):
    if items_dur_fact == None:
      items_dur_fact = self._items_dur_fact
    self.setDurValues(dur=dur, dur_fact=dur_fact, items_dur_fact=items_dur_fact)
    for i, env in enumerate(self._envs):
      env.setDur(self._dur[i])

class ShellAdsr(Shell):
  """
  # @TODO map self._trigs to Adsr objects play method 
  
  Wraps a number of Adsr pyo objects.
  
  :Args:
    dur: Adsr dur
    num: number of Adrs objects
    dur_fact: multiplier for the Adsr dur parameter
  """
  def __init__(self, dur, num=1, dur_fact=1):
    Shell.__init__(self, num=num, dur=dur, dur_fact=dur_fact)
    self._envs = [Adsr(attack=self._dur*.05, decay=self._dur*.25, sustain=.6, release=self._dur*.1, dur=self._dur, mul=num*.1)
      for i in range(1, num+1)]
    self._trigs = self._envs


  # Set the shape of the Adsr
  def setShellDur(self, dur):
    dur = dur*self._dur_fact
    self._dur = dur
    for env in self._envs:
      env.setAttack(dur*.05)
      env.setDecay(dur*.25)
      env.setSustain(.6)
      env.setRelease(dur*.1)
      env.setDur(dur)

if __name__ == '__main__':
  from pitches import *
  from random import randint
  from random import choice

  s = Server().boot()
  p = Pitches(degrees=[0,1,2,3,4,5,6,7], tuning='harmonic')
#   p = Pitches(degrees=[0,4,7,12], tuning='just')
  beat_time = Sig(.15)
  shells = [
    ShellHann(dur=beat_time.value, num=8, dur_fact=.5, items_dur_fact=[.5, .45, .4, .35, .3, .25, .2, .15]),
    ShellHann(dur=beat_time.value, num=8, dur_fact=.9, items_dur_fact=[.4, .05, .04, .035, .03, .025, .02, .05]),
    ShellHann(dur=beat_time.value, num=8, dur_fact=.6, items_dur_fact=[.02, .05, .03, .3, .03, .4, .2, .25])
  ]
  m = Metro(beat_time, poly=1).play()
  
  # Generate the envelope manager
  env = ShellManager(shell=shells[0])
  sin = Sine(freq=p.getPitches(), mul=env.getShell())
  mix = Pan(sin).out()
  
  count = 0
  def play_me():
    global count
    if count%3==0:
      root = 100*randint(2,6)
      p.setRoot(root)
      
    bt = choice([.15, .3, .15, .15, .6, .15, .3])
    beat_time.setValue(bt)
    shell_num = randint(0,2)
    env.setShell(shells[shell_num])
    env.setShellDur(beat_time.value)
 
    env.play()
    count += 1
  
  tf = TrigFunc(m, play_me)
  s.gui(locals())  
    