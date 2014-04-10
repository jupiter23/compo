from pyo import *
from pitches import Pitches
from shell import *
from move import *
from random import randint
from random import choice

s = Server().boot()

# Generate the pitches manager (see pitches.py)
p = Pitches(degrees=[0,4,7], tuning='just')

beat_time = Sig(.3)
m = Metro(beat_time, poly=1).play()

# Generate Adsr envelopes (see shell.py)
# shells = [
#   ShellAdsr(dur=beat_time.value, dur_fact=.4, num=p.len),
#   ShellAdsr(dur=beat_time.value, dur_fact=.8, num=p.len)
# ]

# Generate Adsr envelopes (see shell.py)
shells = [
  ShellHann(dur=beat_time.value, dur_fact=.4, num=p.len),
  ShellHann(dur=beat_time.value, dur_fact=.8, num=p.len)
]
 
# Generate the envelope manager (see shell.py)
env = ShellManager(shell=shells[1])

sin = Sine(freq=p.getPitches(), mul=env.getShell())
mix = Pan(sin).out()

count = 0

# Strummer move (see move.py)
strum = Strummer(inst=env)

def test_strum():
  global count

  # Set a random value for the metro time.
  beat_time.setValue(randint(4,6)*.1)
  print 'beat_time.value: ', beat_time.value

  # Select envelopes to read.
  shell_num = randint(0,1)
  print 'shell num: ', shell_num

  # Update the envelope durations (env is an instance of ShellManager
  env.setShell(shells[shell_num])
  env.setShellDur(beat_time.value*.5)
  
  
  # @TODO the following calculations should be done within the Strummer class.
  
  # diff_time the difference between the metro time and the envelope time.  
  diff_time = beat_time.value - env.getShellDur()

  # Lapse_value is diff_time divided by the number of envelopes to read.
  # The first envelope should be read at 0, and each subsequent envelope at lapse_value * i where i is
  # the enveloppe's index in the list of envelopes, up to i = n - 1 where n is the number of envelopes. 
  lapse_value = diff_time / env.getLen()

  # strum is an instance of Strummer    
  strum.setLapse(lapse_value)
  strum.strum()
  
  count+=1
  
tf = TrigFunc(m, test_strum)
s.gui(locals())
