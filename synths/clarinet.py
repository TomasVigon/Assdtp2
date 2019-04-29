from . import base_synth
import os   
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from scipy.signal import argrelextrema
import IPython.display as ipd
import warnings
warnings.filterwarnings('ignore')

class clarinet(base_synth):
    """description of class"""

    def __init__(self,fo,fs,length,*args):
        N1=1#N1/N2 definen la relación fc/fm
        N2=2# Para N1 y N2 naturales, fo tiene la forma de fc/N1 o fm/N2
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
        [A, I]=self.woodenv(self.len/5,self.len*3/5,self.len/5,self.fs)
        I=-2*I+4
        y = A*np.cos(2*np.pi*self.fc*self.x + I*np.cos(2*np.pi*self.fm*self.x-np.pi/2)-np.pi/2)
        mx = 1.059*(max(abs(y))) # scale to max pk of -.5 dB
        y = y/mx
        #wavData = np.asarray(32000*y, dtype = np.int16)
        self.wavData = y
        #write('clarinet.wav', self.fs, self.wavData) #Para probar el audio puede exportarse a wav
        #plt.plot(y, label = "clarinet") #Para probar el audio puede verse su forma
        #plt.xlabel('Milliseconds')
        #plt.title('Source Waveform')
        #plt.grid(True)
        #plt.show()

    def woodenv(self,attackT,sustainT,releaseT,fs):
	
        atime=np.arange(0,attackT-1/fs, 1/fs)
        yatt= np.exp(atime/attackT*1.5)-1#creo la exponencial creciente asociada al ataque
        yatt=yatt/np.max(yatt)
        temp =np.ones(np.round(int(sustainT*fs)))
        y1=np.concatenate((yatt , temp))

        rem1=(len(self.x)-len(y1))/4
        rtime1=np.arange(0,rem1/fs, 1/fs)
        rtime2=np.arange(0,3*rem1/fs, 1/fs)
        k=0.95
        yrel1=2-np.exp(-rtime1*4*np.log(1/(2-k))/releaseT)
        yrel2=np.exp(-rtime2*(4/3)*np.log(1/(1-k))/releaseT)-(1-k)#creo la exponencial decreciente asociada al release

        ymod=np.concatenate((y1, np.ones(len(self.x)-len(y1))))
        yamp=np.concatenate((y1, yrel1, yrel2))
        yamp=np.resize(yamp,(len(self.x)))
        return [yamp, ymod]
    