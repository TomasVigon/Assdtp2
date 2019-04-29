from . import base_synth
import os   
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from scipy.signal import argrelextrema
import IPython.display as ipd
import warnings
warnings.filterwarnings('ignore')

class trumpet(base_synth):
    """description of class"""

    def __init__(self,fo,fs,length,*args):
        N1=1#N1/N2 definen la relación fc/fm
        N2=1# Para N1 y N2 naturales, fo tiene la forma de fc/N1 o fm/N2
        self.fo=fo
        self.fc=self.fo*N1
        self.fm=self.fo*N2
        self.fs=fs
        self.len=length
        if self.fo == 0:
            self.fc=args[0]
            self.fm=args[1]
        self.ident = id(self)
        #self.name = '%dHz_carrier-%dHz_mod-%s_Index_%d.wav' % (self.fc, self.fm,self.ident)
        self.x = np.arange(0,self.len, 1.0/self.fs)
        [A, I]=self.brassenv(self.len/6,self.len/6,self.len/2,self.len/6,self.fs)
        I=10*I
        y = A*np.cos(2*np.pi*self.fc*self.x + I*np.cos(2*np.pi*self.fm*self.x-np.pi/2)-np.pi/2)
        mx = 1.059*(max(abs(y))) # scale to max pk of -.5 dB
        y = y/mx
        #wavData = np.asarray(32000*y, dtype = np.int16)
        self.wavData = y
        #write('trumpet.wav', self.fs, self.wavData) #Para probar el audio puede exportarse a wav
        #plt.plot(y, label = "trumpet") #Para probar el audio puede verse su forma
        #plt.xlabel('Milliseconds')
        #plt.title('Source Waveform')
        #plt.grid(True)
        #plt.show()

    def brassenv(self,attackT,sustainT1,sustainT2,releaseT,fs):
        atime=np.arange(0,attackT-1/fs, 1/fs)
        yatt= atime/attackT
        stime1=np.arange(0,sustainT1-1/fs,1/fs)
        ysus1=1-stime1/(4*sustainT1)
        stime2=np.arange(0,sustainT2-1/fs,1/fs)
        ysus2=0.75-stime2*3/(20*sustainT2)
        rtime=np.arange(0,releaseT-1/fs,1/fs)
        yrel=0.6-rtime*3/(5*releaseT)
        y=np.concatenate((yatt,ysus1,ysus2,yrel))
        y=np.resize(y,(len(self.x)))
        return [y, y]




