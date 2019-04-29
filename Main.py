import mido as mido
import os   
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from scipy.signal import argrelextrema
import IPython.display as ipd
import warnings
warnings.filterwarnings('ignore')
import soundfile as sf
import numpy as np
#import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.pylab as pyl
import scipy.io.wavfile
from scipy import signal
import sounddevice as sd
import math
import synths
print("'La Buroracia es todo aquello que no es la esencia de las ideas' -Ari 2019 ")
mid = mido.MidiFile('Pirates of the Caribbean.mid')
#tempo = 120
#ticks = mid.ticks_per_beat()
Time=0
key='C'
ticks = mid.ticks_per_beat
arregloDeTracks = []
variabledetracks=0
class Parametros:
  velocidad = None
  channel = None
  t = None
  def __init__(self,velocidad,channel,t):
      self.velocidad= velocidad
      self.channel= channel
      self.t= t

tempoind=0
arreglotempos = []
FlagDePrimerTrack=1
for track in mid.tracks:
     #itero por todos los elementos o mensajes de mi archivo midi
     #itero primero para ver de buscar mi tempo, deberia aparecer antes que mis notas. Predeterminado 120bpm 
     #Guardo por cada iteracion para cada nota los tiempos y los parametros
     #Estructura: Diccionario de arreglos en los que cada key es la nota y cada arreglo contiene Objeto Paramtetro con tiempo channel y velocidad 
  print(track)
  #print(b.istrack())
  NoteDictionary  = {}
  CurrentTime = 0
  CurrentTImeTempos=0
  tempoanterior=0
  if(FlagDePrimerTrack):
    #Estoy en el primer track donde me pasan las configuraciones
    for message in track:
      tempoanterior=message.time
      CurrentTImeTempos + mido.tick2second(message.time,ticks,tempoanterior)
      if(message.type=='set_tempo'):
        arreglotempos.append([message.tempo,CurrentTImeTempos])  
    FlagDePrimerTrack=0

  for message in track:
    
      if(len(arreglotempos) > 1): ##si hay varios tiempos entonces NO HAY TEMPOS EN TRACKS
        tempoind=arreglotempos[0][0]
        for g in range(len(arreglotempos)-1):
          if(Time<arreglotempos[g+1][1] and Time>arreglotempos[g][1]):
            tempoind=arreglotempos[g][0]
      else:
        if(message.type=='set_tempo'): 
          tempoind=message.tempo
          
      CurrentTime = CurrentTime + mido.tick2second(message.time,ticks,tempoind)
      if(message.type=='note_on' or message.type == 'note_off'):
          if not message.note in NoteDictionary:
            NoteDictionary[message.note] = []
            NoteDictionary[message.note].append(Parametros(message.velocity,message.channel,CurrentTime))
          else:   
            NoteDictionary[message.note].append(Parametros(message.velocity,message.channel,CurrentTime))
  if(len(NoteDictionary)!=0):
      
      if (track.name==''):
          arregloDeTracks.append(['track'+ str(variabledetracks) ,NoteDictionary])
          variabledetracks=variabledetracks+1
      else:    
          arregloDeTracks.append([track.name,NoteDictionary])              

print('hola')
def note2Frec(n):
  f=((2**((n-69)/12)))*440
  return f


fs = 44100
#y = Bell.Bell(440,2000,5,5,2).getVector() #(fo,fs,Duracion,Ao=,Io=2)
#y = y.tolist() #ojo tiene valores muy altos
Time = mid.length
print('time =',Time)
CancionTrack = np.arange(0,Time,1/fs)
CancionTrack = np.asarray(CancionTrack)
Cancion = CancionTrack
for index in range(len(CancionTrack)):
      Cancion[index]=0
      CancionTrack[index]=0
print(len(Cancion))
arregloDeCancionesTrack=[]


"""

tengo aca que poder asignar tracks a instrumentos. Ya tengo la lista de tracks.
sps cuando entro al for en la condicion de if pongo if(track[0]= tal asignar tal)
poder desactivar canales


"""




for track in arregloDeTracks:

  print(track[0])
  y = []
 # for index in range(len(Cancion)):
    #Cancion[index]=0  
   
      #track[1] tiene el Notediccionary asociado a cada track
  for nota in track[1] :
    print(nota)
    for i in range(len(track[1].get(nota))-1):
      if i%2 == 0 : #Asumo que todas las notas impares son Velocity=0
        deltaT = track[1].get(nota)[i+1].t-track[1].get(nota)[i].t
        Fo = note2Frec(nota)
        if(Fo<20 or Fo>20000):
          print('Estas haciendo cualquiera')
        tiempoinicial= track[1].get(nota)[i].t
        if(tiempoinicial==0 and deltaT!=0):
          print("meestajodiendo")   
        if(deltaT!=0):
          #La burocracia: 
          if(track[0]=='Right Hand'):
            y=synths.create("clarinet",Fo,fs,deltaT).getVector() 
          else:   
            y=synths.create("trumpet",Fo,fs,deltaT,track[1].get(nota)[i].velocidad,2).getVector()    
          for j in range(len(y)):
            Cancion[int(tiempoinicial*fs)+j]= Cancion[int(tiempoinicial*fs)+j]+y[j]
          if(math.isnan(Cancion[2346])):
               print("LA CAGUEEEEEEEEEEEEEEEEEEEEEEE")
           #paso de float a in
    
                    #print(y[0],y[1],y[2],y[234])
  #if(not math.isnan(np.amax(Cancion))):      
  #  Cancion= Cancion/np.amax(Cancion)
  


 # if(len(Cancion)!=0):
  #  Cancion = Cancion/np.amax(Cancion)
   # arregloDeCancionesTrack.append(Cancion)
   # for w in range(len(Cancion)):
   #     Cancion[w]=0
  #if(len(y)>1): #evito que meta tracks sin notas
  
    #arregloDeCancionesTrack.append(Cancion)
            
#Cancion=Cancion/np.amax(Cancion)
#for i in range(len(arregloDeCancionesTrack)-1):
# print('Adding Tracks')
# arregloDeCancionesTrack[0] += arregloDeCancionesTrack[i+1]
 #arregloDeCancionesTrack[0] = arregloDeCancionesTrack[0]/2

Cancion=Cancion/12

FileName = 'CancionExportada.wav'
print('Exporting 2 wav',FileName)
wavData = np.asarray(50000*Cancion,dtype = np.int16)       
write(FileName,fs, wavData)
#f.write('Cancion.wav', CancionFinal, fs)