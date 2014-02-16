from pyo import *

class Sinux():
  def __init__(self, notes=[]):
    self.notes = notes
    num_notes = len(notes)
    self.sins = [Sine(freq=n, mul=1./num_notes) for n in notes]
    self.mix = Mix(self.sins, voices=2)
    
  def play(self):
    self.mix.out()
  
  def stop(self):
    self.mix.stop()
      
if __name__ == '__main__':
  from notes import Notes
  s = Server().boot()
  n = Notes()
  n.setNotesByChromaticPos(tuning='just', degrees=[1,5,8])
  sinux = Sinux(n.getNotes())
  sinux.play()
  s.gui(locals())