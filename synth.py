from pyo import *
from shell import *

class RissetSnare(Shell):
  """
  Implementation of Risset Snare as described in Computer Music, Dodge, 1997.
  This class inherits the Shell class and manages its envelopes.
  
  """
  def __init__(self, pitches, dur, dur_fact=1):
    Shell.__init__(self, dur, num=1, dur_fact=1)
    self.f1 = ExpTable(list=[(0, 0.0), (32, 1.0), (8192, 0.0)], exp=10)
    self.f2 = ExpTable(list=[(0, 0.0), (32, 1.0), (8192, 0.0)], exp=15)
    self.t1 = TrigEnv(Trig(), table=self.f1, dur=dur, mul=.09)
    self.t2 = TrigEnv(Trig(), table=self.f2, dur=dur, mul=.07)
    self.randi = Randi(freq=400, mul=self.t2)
    self.noise = Sine(freq=500, mul=self.randi)
   
    # Wrap the envelopes
    self._envs = EnvWrap([self.t1, self.t2])
    
    # Keep the Sig objects
    self.pitches = pitches.getPitches()
    self.num = len(self.pitches)
    self.inharms = [0 for x in range(0, self.num)]
    self.funds = [0 for x in range(0, self.num)]
    for i, pitch in enumerate(self.pitches):
      self.inharms[i] = Sine(freq=[pitch, pitch*1.6, pitch*2.2, pitch*2.3], mul=[.5, .75, 1., .75]) * .006 * self.t2 
      self.funds[i] = Sine(freq=pitch, mul=self.t1) 
    
  def setShellDur(self, dur):
    self.t1.setDur(dur)
    self.t2.setDur(dur)

  def out(self):
    return Mix([self.noise + self.inharms[i] + self.funds[i] for i in range(0, self.num)], mul=1./self.num).out()

class Ring426():
  def __init__(self):
    rand = Randi(freq=500)
    self.sine = Sine(freq=200, mul=rand)
  
  def out(self):
    return self.sine.out()
    
if __name__ == '__main__':
  from pitches import Pitches
  s = Server().boot()
#  p = Pitches(degrees=[0, 7, 10, 12], root=400)
  p = Pitches(degrees=[0], root=300)
  snr = RissetSnare(pitches=p, dur=2)
  out = Mix(snr.out(), voices=2).out()
  env = snr.getEnvs()
  m = Metro(time=3).play()
  
  def play_me():
    env.play()
    
  tf = TrigFunc(m, play_me)
 
  if False:
    dur = 0.5
    freq = 400
    f1 = ExpTable(list=[(0, 0.0), (32, 1.0), (8192, 0.0)], exp=10)
    f2 = ExpTable(list=[(0, 0.0), (32, 1.0), (8192, 0.0)], exp=15)
  #  osc_f1 = Osc(table=f1, freq=0.5, mul=.25)
  #  osc_f2 = Osc(table=f2, freq=0.5, mul=.3) 
    m = Metro(time=2).play()
    t1 = TrigEnv(m, table=f1, dur=1, mul=.25)
    t2 = TrigEnv(m, table=f2, dur=1, mul=.3)
    
  #  t1 = OscTrig(table=f1, trig=m, freq=2, mul=.25)
  #  t2 = OscTrig(table=f2, trig=m, freq=2, mul=.3)
    randi = Randi(freq=400, mul=t1)
    noise = Sine(freq=500, mul=randi)
    inharm = Sine(freq=[freq, freq*1.6, freq*2.2, freq*2.3], mul=[.5, .75, 1., .75]) *.1 * t2 
    fund = Sine(freq=freq, mul=t1)
    mix = Mix(noise+fund+inharm, voices=2, mul=1).out()
  
#   spec = Spectrum(sine)
  s.gui(locals())
  