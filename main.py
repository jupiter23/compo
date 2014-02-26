from pyo import *
from pitches import Pitches
from shell import *
from move import *
from random import randint
from random import choice

s = Server().boot()

# Generate the pitches manager (see pitches.py)
p = Pitches(degrees=[0,4,7], tuning='just')

beat_time = Sig(.2)
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


# Strummer move (see move.py)
strum = Strummer(inst=env)

count = 0
def play_me3():
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
  
tf = TrigFunc(m, play_me3)

s.gui(locals())




# Another test
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
    env.setEnvs(shells[shell_num])
    env.setEnvsDur(beat_time.value)
  else:
    p.setDegrees(pos=[1], degrees=[3])

  env.play()
  count += 1







# MORE STUFF
if (False):
  env1 = Adsr(dur=0.5)
  env2 = Adsr(dur=0.25)
  env = Sig(env1)


  def play_me():
    global count
    if (count %2):
      env.setValue(env2)
      env2.play()
    else:
      env.setValue(env1)
      env1.play()
    count += 1


#sin = Sine(freq=200, mul=env).out()
#m = Metro(1, poly=1).play()
#te = TrigFunc(m, play_me)

#tf = TrigFunc(m, snd.play)
#te = TrigEnv(m, table=env, dur=.25, mul=.2)

if(False):
  snd = SoundAdsr()
  print len(snd.getEnvs());
  env = HannTable()
  p = Pitches(degrees=[0,5,7])
  m = Metro(.5, poly=1).play()
  te = TrigEnv(m, table=env, dur=.25, mul=.2)
#  tf = TrigFunc(m, notes.getNote)
  sin = Sine(freq=p.getPitches(), mul=te).out()
