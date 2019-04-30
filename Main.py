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
import matplotlib.pyplot as plt
import matplotlib.pylab as pyl
import scipy.io.wavfile
from scipy import signal
import sounddevice as sd
import math
import synths

print("'La Buroracia es todo aquello que no es la esencia de las ideas' -Ari 2019 ")

#---------------------------------------Comunicacion con el usuario: Elegir Archivo y Activar Espectograma-------

print("Insertar nombre de Archivo")
nombredeArchivo = input()
print("Espectograma ON? Y/N")
rta=input()
if(rta=='Y' or rta=='y'):
  BooleanEspectograma=1
elif(rta=='n' or rta=='N'):
  BooleanEspectograma=0
else:
  print("hiciste cualquiera monki")
  exit()

#----------------------------------------------------------------------------------------------------------------

mid = mido.MidiFile(str(nombredeArchivo +'.mid'))
Time=0
ticks = mid.ticks_per_beat
arregloDeTracks = []
variabledetracks=0
tempoind=0
arreglotempos = []
FlagDePrimerTrack=1
fs = 44100

def note2Frec(n):
  f=((2**((n-69)/12)))*440
  return f
def Espectograma(vector,fs,*window):
  f,t,sx=signal.spectrogram(vector,fs,window)
  plt.pcolormesh(t, f, sx)
  plt.show()
  return


class Parametros:
  velocidad = None
  channel = None
  t = None
  def __init__(self,velocidad,channel,t):
      self.velocidad= velocidad
      self.channel= channel
      self.t= t

print('Parsing Midi...')

for track in mid.tracks:
     #itero por todos los elementos o mensajes de mi archivo midi
     #itero primero para ver de buscar mi tempo: saco del arreglo de tempos ó de mi track 
     #Guardo por cada iteracion para cada nota los tiempos y los parametros en NoteDictionary
     #Estructura: Diccionario de arreglos en los que cada key es la nota y cada arreglo contiene Objeto Paramtetro con tiempo channel y velocidad 
  
  print('Parsing... ',track)
  NoteDictionary  = {}
  CurrentTime = 0
  CurrentTimeTempos=0
  tempoanterior=0
  if(FlagDePrimerTrack):
    #Parseo el primer track para ver si tiene estipulados todos los tempos de la cancion.
    #De ser asi creo mi vector de tempos en donde coloco el valor del tempo y el tiempo en s en el que ocurre
    for message in track:
      tempoanterior=message.time
      CurrentTimeTempos + mido.tick2second(message.time,ticks,tempoanterior)
      if(message.type=='set_tempo'):
        arreglotempos.append([message.tempo,CurrentTimeTempos])  
    FlagDePrimerTrack=0

  for message in track:
    
      if(len(arreglotempos) > 1): ##si hay arreglo de tempos entonces me muevo con esto para fijar mi tempo
        tempoind=arreglotempos[0][0] ##a medida que avanzo guardo 
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
  
  #Armo un arreglo con todos los tracks y sus nombres (si no tiene se lo asigno)
  #Esto me sirve para despues asignar instrumentos a cada track
  if(len(NoteDictionary)!=0):      
      if (track.name==''):
          arregloDeTracks.append(['track'+ str(variabledetracks) ,NoteDictionary])
          variabledetracks=variabledetracks+1
      else:    
          arregloDeTracks.append([track.name,NoteDictionary])              

print('Midi Parsed')
Time = mid.length
print('Total Midi Time =',Time)

##---------------------------------------Comunicacion con Usuario: elegir instrumentos---------------------------
nombreDeTracks=[]
nombreDeInstrumentos=[]

print("Elegir los instrumentos: bell clarinet trumpet para cada uno de los siguientes tracks")

for tracka in arregloDeTracks:
  nombreDeTracks.append(tracka[0])

print(nombreDeTracks)


while (len(nombreDeInstrumentos)!=len(nombreDeTracks)):
  instr= input()
  if(instr=='bell' or instr=='clarinet' or instr=='trumpet' or instr==''):
    nombreDeInstrumentos.append(instr)
  else:
    print("Hiciste cualquiera monki")
    exit()

print(nombreDeInstrumentos)

##---------------------------------------------------------------------------------------------------------------


##---------------------------------------Sintetizando tacks------------------------------------------------------

print("Sintetizando...")
#Creo vectores
CancionTrack = np.arange(0,Time,1/fs)
CancionTrack = np.asarray(CancionTrack)
Cancion = CancionTrack
#Inicializando vectores en 0
for index in range(len(CancionTrack)):
      Cancion[index]=0
      CancionTrack[index]=0
print("Longitud Vector: " ,len(Cancion))

arregloDeCancionesTrack=[]
contadorDeInstrumentos=0
for track in arregloDeTracks:

  print('Sintetizando: ' ,track[0])
  y = [] 
  print('Con Instrumento: ' ,nombreDeInstrumentos[contadorDeInstrumentos])

  for nota in track[1] :
    print('Nota: ',nota)
    for i in range(len(track[1].get(nota))-1):
      if i%2 == 0 : #Asumo que todas las notas impares son Velocity=0
        deltaT = track[1].get(nota)[i+1].t-track[1].get(nota)[i].t
        Fo = note2Frec(nota)
        tiempoinicial= track[1].get(nota)[i].t
        if(deltaT!=0 and nombreDeInstrumentos[contadorDeInstrumentos]!=''):   
          y=synths.create(nombreDeInstrumentos[contadorDeInstrumentos],Fo,fs,deltaT,track[1].get(nota)[i].velocidad,2).getVector()    
          for j in range(len(y)):
            Cancion[int(tiempoinicial*fs)+j]= Cancion[int(tiempoinicial*fs)+j]+y[j] 
  contadorDeInstrumentos=contadorDeInstrumentos+1         

Cancion=Cancion/12
print("Fin de Sintetización")

FileName = 'CancionExportada.wav'
print('Exporting 2 wav',FileName)
wavData = np.asarray(50000*Cancion,dtype = np.int16)       
write(FileName,fs, wavData)

#if(BooleanEspectograma):
 # print("Expectograma: ")
 # Espectograma(Cancion,fs)