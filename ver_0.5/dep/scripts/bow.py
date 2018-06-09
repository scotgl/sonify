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




pan = 0
index = 10
cs = ctcsound.Csound()

csd = '''
<CsoundSynthesizer>
<CsOptions>
-odac -d

</CsOptions>
<CsInstruments>

sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 1

instr 1

;aMod1 poscil 200, 700, 1
aMod1 poscil p4, p5, 1   ; p4 = amp1, p5 = f1, p6 = amp2, p7 = f2 
;aMod2 poscil 1800, 290, 1
aMod2 poscil p6, p7, 1
kenv linen p9 , 0.3 , p3, p9
aSig poscil kenv, 440+aMod1+aMod2, 1
outs aSig*(1-p8), aSig*p8
endin



</CsInstruments>
<CsScore>
f 0 14400
f 1 0 1024 10 1 

</CsScore>

</CsoundSynthesizer>
'''

cs.compileCsdText(csd)
cs.start()
pt = ctcsound.CsoundPerformanceThread(cs.csound())
pt.play()

def f(percentage):
	global index
	index = percentage
	

def on_button_clicked(b):
    in_min  = 0
    in_max = 100
    out_min=690
    out_max = 710

	
    global index
    tts = gTTS(text=(str(index)+'percent'), lang='en')
    tts.save("num.mp3")
    os.system("afplay num.mp3")
    if (index>50):
        pan = 1
    if (index<50):
        pan = 0
    if (index==50):
        pan = 0.5
    freq = (index - in_min) * (out_max - out_min) / (in_max - in_min) + out_min  
    #print(freq)  
	
    pt.scoreEvent(False, 'i', (1, 0, 4, 200, 700, 200, freq, pan, 0.5))
    

