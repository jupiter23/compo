from pyo import *

class Sinux():
  def __init__(self, pitches, envs):
    self._pitches = pitches
    num_notes = len(pitches)
    self.sins = [Sine(freq=n, mul=1./num_notes) for n in pitches]
    self.mix = Mix(self.sins, voices=2)
    
  def play(self):
    self.mix.out()
  
  def stop(self):
    self.mix.stop()
      
if __name__ == '__main__':
  from pitches import Pitches
  s = Server().boot()
  n = Pitches(root=200, degrees=[0,4,7,11])
  sinux = Sinux(n.getPitches())
  sinux.play()
  s.gui(locals())