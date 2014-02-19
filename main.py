from pyo import *
from pitches import Pitches
from shell import *
from random import randint
from random import choice

s = Server().boot()
beat_time = Sig(0.3)

count = 0
# Generate the pitches manager
p = Pitches(degrees=[0,5,7], tuning='just')

# Generate Adsr envelopes
shells = [
  ShellAdsr(dur=beat_time.value, dur_fact=.8, num=p.len),
  ShellAdsr(dur=beat_time.value, dur_fact=.5,num=p.len)
]

# Generate the envelope manager
env = ShellMode(p.len, shells[0].getEnvs())

sin = Sine(freq=p.getPitches(), mul=env.getEnvs()).out()
m = Metro(beat_time, poly=1).play()

def play_me2():
  global count
  if (count%3==0):
    beat_time.setValue(randint(2, 8)*.1)
    env.setEnvs(shells[randint(0,1)].getEnvs())
  
  if (count%2==0):
    p.setDegrees(pos=[1], degrees=[4])
  else:
    p.setDegrees(pos=[1], degrees=[3])

  if (count%4==0):
    p.setRoot(100*randint(3,5))
    p.setDegrees(pos=[2], degrees=[randint(7,12)])

  env.play()
  count += 1

def update_durs():
  for shell in shells:
    shell.setEnvsDur(beat_time.value)

c = Change(beat_time)
t = TrigFunc(c, update_durs)
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
