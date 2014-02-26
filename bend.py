from pyo import *
from pitches import Pitches
from shell import *
from move import *
from random import randint
from random import choice

s = Server().boot()

# Generate the pitches manager (see pitches.py)
p = Pitches(degrees=[0,2], tuning='just', root=400)

beat_time = Sig(1)
m = Metro(beat_time, poly=1).play()
m2 = Metro(2).play()

# Generate Adsr envelopes (see shell.py)
shells = [
  ShellAdsr(dur=beat_time.value, dur_fact=.4, num=p.len),
  ShellAdsr(dur=beat_time.value, dur_fact=.8, num=p.len)
]
 
# Generate the envelope manager (see shell.py)
env = ShellManager(shell=shells[1])

sin = SuperSaw(freq=p.getPitches(), mul=env.getShell())
mix = Pan(sin).out()

bender = Bender(p, pos=[0], target_freq=[p.getFreqs()[1]], dur=[1.5], go_back_dur=[0.5], go_back=True)
count = 0
def play_me4():
  global count
  if (count%5==4):
    beat_time.setValue(1)
    env.setShellDur(beat_time.value)  
  
  if (count%5==0):
    beat_time.setValue(0.25)  
    env.setShellDur(beat_time.value)  
  
  env.play()
  count += 1

def bend_me():
  bender.bend()

tf = TrigFunc(m, play_me4)
tf2 = TrigFunc(m2, bend_me)

s.gui(locals())
