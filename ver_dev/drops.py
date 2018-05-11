from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from IPython.display import display
from gtts import gTTS
import os


import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline

import pandas as pd
import ctcsound

index = 10
cs = ctcsound.Csound()

csd_drop = '''
<CsoundSynthesizer>
<CsOptions>
-o dac
</CsOptions>
<CsInstruments>
;Example by Joachim Heintz
sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 1

giSine    ftgen     0, 0, 2^10, 10, 1

instr 1 ;master instrument
inumparts =         p4 ;number of partials
ibasfreq  =         200 ;base frequency
ipart     =         1 ;count variable for loop
;loop for inumparts over the ipart variable
;and trigger inumpartss instanes of the subinstrument
loop:
ifreq     =         ibasfreq * ipart
iamp      =         1/ipart/inumparts
          event_i   "i", 10, 0, p3, ifreq, iamp
          loop_le   ipart, 1, inumparts, loop
endin

instr 10 ;subinstrument for playing one partial
ifreq     =         p4 ;frequency of this partial
iamp      =         p5 ;amplitude of this partial
aenv      transeg   0, .01, 0, iamp, p3-0.1, -10, 0
apart     poscil    aenv, ifreq, giSine
          outs      apart, apart
endin



</CsInstruments>
<CsScore>
f 0 14400
f 1 0 1024 10 1 

</CsScore>

</CsoundSynthesizer>
'''

cs.compileCsdText(csd_drop)
cs.start()
pt = ctcsound.CsoundPerformanceThread(cs.csound())
pt.play()

def f(percentage):
    global index
    index = percentage


def on_button_clicked(b):
    in_min  = 0
    in_max = 100
    out_min=1
    out_max = 20


    global index
    tts = gTTS(text=(str(index)+'percent'), lang='en')
    tts.save("num.mp3")
    os.system("afplay num.mp3")
    
    freq = (index - in_min) * (out_max - out_min) / (in_max - in_min) + out_min  
    #print(freq)  

    pt.scoreEvent(False, 'i', (1, 0, 3, freq))
    
    

