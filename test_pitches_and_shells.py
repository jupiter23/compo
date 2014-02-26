from pyo import *
from pitches import Pitches
from shell import *
from move import *
from random import randint
from random import choice

s = Server().boot()

# Generate the pitches manager (see pitches.py)
p = Pitches(degrees=[0,4,7], tuning='just')

beat_time = Sig(2)
m = Metro(beat_time, poly=1).play()

# Generate Adsr envelopes (see shell.py)
shells = [
  ShellAdsr(dur=beat_time.value, dur_fact=.4, num=p.len),
  ShellAdsr(dur=beat_time.value, dur_fact=.8, num=p.len)
]
 
# Generate the envelope manager (see shell.py)
env = ShellManager(shell=shells[1])

sin = Sine(freq=p.getPitches(), mul=env.getShell())
mix = Pan(sin).out()

count = 0
def play_me2():
  global count

  if (count%4==0):
    root = 100*randint(2,6)
    p.setRoot(root)
    p.setDegrees(pos=[2], degrees=[randint(7,12)])

  if (count%2==0):
    p.setDegrees(pos=[1], degrees=[4])
    bt = randint(2,6) *.1
    beat_time.setValue(bt)
    shell_num = randint(0,1)
    env.setShell(shells[shell_num])
    env.setShellDur(beat_time.value)
  else:
    p.setDegrees(pos=[1], degrees=[3])

  env.play()
  count += 1

tf = TrigFunc(m, play_me2)
s.gui(locals())
