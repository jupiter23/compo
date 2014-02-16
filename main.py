from pyo import *
from pitches import Pitches
from random import randint

s = Server().boot()
s.start()
s.gui(locals())

p = Pitches()



#env = HannTable()
#m = Metro(.125, poly=2).play()
#te = TrigEnv(m, table=env, dur=.25, mul=.2)
#tf = TrigFunc(m, notes.getNote)
#s = Sine(notes).out()