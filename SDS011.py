import serial
from datetime import datetime
import time
import numpy as np

"""
#Variables #########################
DEFAULT_SERIAL_PORT = "/dev/ttyUSB0"

sample = 10 #Variable de moyennage en secondes
"""

#Classes ###
class SDS011:
    "Objet SDS011"
    def __init__(self,port = "/dev/ttyUSB0"):
        self.port = port
        
    def acquisition(self):
        "Acquisition données PM2.5 et PM10 depuis un SDS011"
        capteur = serial.Serial(self.port)
        byte = capteur.read()
        #print(byte)
        if byte == b'\xaa':
            sentence = capteur.read(size=9) # Read 8 more bytes
            #print ("Sentence size {}".format(len(sentence)))
            #print("sentence: ",sentence)
            PM25= (sentence[1]+sentence[2])/10
            PM10 = (sentence[3]+sentence[4])/10
            line = "PM 2.5: {} μg/m^3  PM 10: {} μg/m^3".format(PM25, PM10)
            # ignoring the checksum and message tail
            print(datetime.now().strftime("%d %b %Y %H:%M:%S: ")+line)
            return {"PM2.5":PM25,"PM10":PM10}
        else:
            print("Pas de données valides")
            return {"PM2.5":'',"PM10":''}
            
    
    def moyenne(self,sample):
        i=0
        PM25list = list()
        PM10list = list()
        while i<=sample:
            res = self.acquisition()
            if res['PM2.5'] !='': PM25list.append(res['PM2.5'])
            if res['PM10'] !='': PM10list.append(res['PM10'])
            i+=1
        PM25res = np.array(PM25list)
        PM25mean = PM25res.mean()  #Moyenne PM25
        PM10res = np.array(PM10list)
        PM10mean = PM10res.mean()  #Moyenne PM10
        print('\n')
        print("----")
        print("{}: Moyenne : PM2.5 {} , PM10 {}".format(datetime.now().strftime("%d %b %Y %H:%M:%S"),round(PM25mean,3),round(PM10mean,3)))
        print("----")
        print('\n')
        return {"PM2.5":round(PM25mean,2),"PM10":round(PM10mean,2)}
"""
#Corps du programme
test = SDS011()
while True:
    res = test.moyenne(sample)
"""

    

