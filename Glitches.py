#!/usr/bin/env python
# encoding: utf-8
from pyo import *
import random

class Instrument:
    def __init__(self):
        pass

    def out(self, delay=0, dur=0):
        self.play(delay=delay, dur=dur)
        self.outsig.out(0, 1, delay=delay, dur=dur)
        return self

    def sig(self):
        return self.outsig

class Sparks(Instrument):
    def __init__(self, mul=1):
        self.env = LinTable([(0,0.0000),(0,1.0000),(2078,1.0000),(2113,0.2448),(8174,0.2448),(8192,0.0000)])
        self.dens = Expseg([(0,0), (60,100)], exp=10)
        self.middur = Expseg([(0,0.25), (60,0.05)], inverse=False, exp=6)
        self.trig = Cloud(density=self.dens, poly=2)
        self.dur = TrigRand(self.trig, min=self.middur*0.5, max=self.middur*1.5).stop()
        self.amp = TrigEnv(self.trig, self.env, dur=self.dur, mul=0.02).stop()
        self.lff = Sine(.1).range(4000, 5000).stop()
        self.outsig = SineLoop(freq=self.lff, feedback=0.4, mul=self.amp*mul).stop()

    def play(self, delay=0, dur=0):
        self.dens.play(delay=delay, dur=dur)
        self.middur.play(delay=delay, dur=dur)
        self.trig.play(delay=delay, dur=dur)
        self.dur.play(delay=delay, dur=dur)
        self.amp.play(delay=delay, dur=dur)
        self.lff.play(delay=delay, dur=dur)
        self.outsig.play(delay=delay, dur=dur)

class Background(Instrument):
    def __init__(self, freq=1000, q=2, mul=1):
        self.gamp = Expseg([(0,0), (20,1), (20.05,0)], exp=4, mul=mul)
        self.lff = Lorenz(0.1, 0.7).range(200, 5000).stop()
        self.lfc = Lorenz(0.05, 0.7).range(0.2, 0.5).stop()
        self.gen = SineLoop(freq=self.lff, feedback=self.lfc, mul=0.01).stop()
        self.outsig = ButBP(self.gen, freq=freq, q=q, mul=self.gamp).stop()

    def play(self, delay=0, dur=0):
        self.gamp.play(delay=delay, dur=dur)
        self.lff.play(delay=delay, dur=dur)
        self.lfc.play(delay=delay, dur=dur)
        self.gen.play(delay=delay, dur=dur)
        self.outsig.play(delay=delay, dur=dur)
        
class Rumble(Instrument):
    def __init__(self, mul=1):
        self.gamp = Fader(fadein=10, fadeout=0.001)
        self.noise = BrownNoise(Randi(min=0.05, max=0.2, freq=[.1,.15]))
        self.lp = ButLP(self.noise, 80, mul=mul)
        self.deg = Degrade(self.lp, bitdepth=5)
        self.rez = Reson(self.deg, freq=[130, 200], q=10, mul=3)
        self.outsig = (self.lp+self.rez) * self.gamp

    def play(self, delay=0, dur=0):
        self.gamp.dur = dur
        self.gamp.play(delay=delay, dur=dur)
        self.noise.play(delay=delay, dur=dur)
        self.lp.play(delay=delay, dur=dur)
        self.deg.play(delay=delay, dur=dur)
        self.rez.play(delay=delay, dur=dur)

class Rhythm(Instrument):
    def __init__(self, freq=2, mul=1):
        self.lf = Sine(random.uniform(.1,.2)).range(.6, .8).stop()
        self.v1 = SineLoop(freq=freq, feedback=self.lf, mul=0.02).stop()
        self.v2 = SineLoop(freq=freq, feedback=self.lf*0.95, mul=0.02).stop()
        self.outsig = Mix([self.v1, self.v2],voices=2, mul=mul)

    def play(self, delay=0, dur=0):        
        self.lf.play(delay=delay, dur=dur)
        self.v1.play(delay=delay, dur=dur)
        self.v2.play(delay=delay, dur=dur)


s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()
s.startoffset = 60

sparks = Sparks(mul=.3).out(delay=10, dur=60)
rumble = Rumble(mul=1).out(dur=70)
back1 = Background(freq=400, q=4, mul=3).out(delay=50, dur=21)
back2 = Background(freq=700, q=4, mul=3).out(delay=50, dur=21)
back3 = Background(freq=2700, q=4, mul=3).out(delay=50, dur=21)

ryth1 = Rhythm(freq=1, mul=.15).out(delay=70, dur=0)
s40 = Sine([40,40.1], mul=0.05).out(delay=70, dur=0)
s80 = Sine([80,80.1], mul=0.025).out(delay=70, dur=0)

env2 = LinTable([(0,0.0000),(0,1.0000),(1694,1.0000),(1694,0.0000),(8192,0.0000)])
rnddur = RandDur(min=[1,1,1,1], max=4)
tenv2 = Change(rnddur)
amp2 = TrigEnv(tenv2, env2, rnddur, mul=0.001)
fr = TrigRand(tenv2, min=5000, max=10000)
syns = Sine(freq=fr, mul=amp2).out(delay=70,dur=0)









s.gui(locals())
