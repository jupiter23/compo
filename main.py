from pyo import *
from pitches import Pitches
from shell import *
from random import randint
from random import choice

s = Server().boot()
beat_time = Sig(1)

count = 0
# Generate the pitches manager
p = Pitches(degrees=[0,5,7], tuning='just')

# Generate Adsr envelopes
shells = [
  ShellAdsr(dur=beat_time.value, dur_fact=.4, num=p.len),
  ShellAdsr(dur=beat_time.value, dur_fact=.8, num=p.len)
]
 
# Generate the envelope manager
env = ShellMode(shell=shells[0])

sin = Sine(freq=p.getPitches(), mul=env.getEnvs())
mix = Pan(sin).out()
m = Metro(beat_time, poly=1).play()

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

tf = TrigFunc(m, play_me2)

s.gui(locals())













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
