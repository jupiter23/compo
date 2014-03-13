from pyo import *
from pitches import Pitches
from shell import *
from move import *
from random import randint
from random import choice

s = Server().boot()

# Generate the pitches manager (see pitches.py)
p = Pitches(degrees=[0,2], tuning='just', root=440)

#long = .45
long = 1
short = long*.25
beat_time = Sig(long)

m = Metro(beat_time, poly=1).play()
m2 = Metro(Sig(long)*2).play()

# Generate Adsr envelopes (see shell.py)
shells = [
  ShellAdsr(dur=beat_time.value, dur_fact=.4, num=p.len),
  ShellAdsr(dur=beat_time.value, dur_fact=.8, num=p.len)
]
 
# Generate the envelope manager (see shell.py)
env = ShellManager(shell=shells[1])

sin = SuperSaw(freq=p.getPitches(), mul=env.getShell())
mix = Pan(sin).out()
freqs=p.getFreqs()

bender = Bender(p, pos=[0], target_freq=[freqs[1]], seg_type='lin', dur=[1.05], go_back_dur=[0.75], go_back=True)
count = 0


def play_me4():
  global count
  if (count%5==4):
    beat_time.setValue(long)
    env.setShellDur(beat_time.value)
  
  if (count%5==0):

    beat_time.setValue(short)  
    env.setShellDur(beat_time.value)  
  
  env.play()
  count += 1

def bend_me():
    root = choice([750,800,755,805,760,765,770,775])*choice([1,1.02,1.03,1.035,1.005])*.0625
#    root = choice([40.8,46,70])*choice([1,1.02,1.03,1.035,1.005])
    p.setRoot(root)
    freqs = p.getFreqs()
    bender = Bender(p, pos=[0], target_freq=[freqs[1]], seg_type='lin', dur=[long*1.05], go_back_dur=[short*3.], go_back=True)
    bender.bend()

# Play the envelopes
tf = TrigFunc(m, play_me4)
# Bend the pitches
tf2 = TrigFunc(m2, bend_me)

s.gui(locals())
