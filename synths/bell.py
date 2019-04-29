from . import base_synth
import os   
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from scipy.signal import argrelextrema
import IPython.display as ipd
import warnings
warnings.filterwarnings('ignore')

class bell(base_synth):

    def __init__(self,fo,fs,length,*args):
        N1=1#N1/N2 definen la relación fc/fm
        N2=2# Para N1 y N2 naturales, fo tiene la forma de fc/N1 o fm/N2
        self.fo=fo
        self.fc=self.fo*N1
        self.fm=self.fo*N2
        self.fs=fs
        self.len=length
        self.Ao=args[0]
        self.Io=args[1]
        if self.fo == 0:
            self.fc=args[2]
            self.fm=args[3]
        self.tau=self.len/10#A partir de la duración de la nota calculo el coeficiente tau
        self.ident = id(self)
        #self.name = '%dHz_carrier-%dHz_mod-%s_Index_%d.wav' % (self.fc, self.fm, str(self.Indm),self.ident)
        x = np.arange(0,self.len, 1.0/self.fs)
        A = self.Ao*np.exp(-x/self.tau)#obtengo la envolvente en amplitud de la señal
        I = self.Io*np.exp(-x/self.tau)#obtengo la envolvente de la modulación en frecuencia
        y = A*np.cos(2*np.pi*self.fc*x + I*np.cos(2*np.pi*self.fm*x-np.pi/2)-np.pi/2)#calculo la señal resultante de modular
        mx = 1.059*(max(abs(y))) # escalo para que el pico máximo sea de -.5 dB
        y = y/mx
        #self.wavData = np.asarray(32000*y, dtype = np.int16)
        self.wavData = y
        #write('bell.wav', self.fs, self.wavData) #Para probar el audio puede exportarse a wav
        #plt.plot(y, label = "bell") #Para probar el audio puede verse su forma
        #plt.xlabel('Milliseconds')
        #plt.title('Source Waveform')
        #plt.grid(True)
        #plt.show()




