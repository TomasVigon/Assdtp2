from abc import ABCMeta, abstractmethod

class base_synth(metaclass=ABCMeta):
    wavData=0
    def __init__(self,fo,fs,length,*args):
        pass 
    def getVector(self):
        return self.wavData

