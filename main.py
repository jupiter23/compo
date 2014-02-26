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

# Strummer move (see move.py)
strum = Strummer(inst=env)

def test_strum():
  global count
  if (count%3==0):
    beat_time.setValue(3)
#    shell_num = 0
  else:
    beat_time.setValue(5)
#    shell_num = 1

  # Set a random value for the metro time.
#  beat_time.setValue(randint(3,5))
  # A glitch is sounded whith values > than the precendent value, but not with values <
  # When new value > previous value, it seems the enveloppe is not read from the beginning.
  print 'beat_time.value: ', beat_time.value

  # Providing a constant value for the metronome does not create glitches.
#  beat_time.setValue(.2)

  # Sellect enveloppes to read.
#  shell_num = randint(0,1)

  shell_num = 1
  # Update the enveloppe durations (env is an instance of ShellManager,
  # shells[shell_num] an instance of ShellAdsr).
  env.setShell(shells[shell_num])
  env.setShellDur(beat_time.value)
  
  # diff_time the difference between the metro time and the enveloppe time.  
  diff_time = beat_time.value - env.getShellDur()

  # Lapse_value is diff_time divided by the number of enveloppes to read.
  # The first enveloppe should be read at 0, and each subsequent enveloppe at lapse_value * i where i is
  # the enveloppe's index in the list of enveloppes, up to i = n - 1 where n is the number of enveloppes. 
  lapse_value = diff_time / env.getLen()

  # strum is an instance of Strummer    
  strum.setLapse(lapse_value)
  strum.strum()
  
  count+=1
  
tf = TrigFunc(m, test_strum)
s.gui(locals())
