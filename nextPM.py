import serial
from datetime import datetime
import time

#Variables #########################
DEFAULT_SERIAL_PORT = "/dev/ttyUSB2"

sample = 1 #Variable de moyennage en secondes


#Classes ###

class NextPM:
    #Classe pour gérer un capteur NextPM de Tera EcologicSense
    def __init__(self,
                 baudrate = 115200,
                 timeout = 1):
        self.serial = serial.Serial(port = DEFAULT_SERIAL_PORT,
                                 baudrate = baudrate,
                                 bytesize=serial.EIGHTBITS,
                                 parity=serial.PARITY_EVEN,
                                 stopbits=serial.STOPBITS_ONE,
                                 timeout = 1)
        
    def parametrage(self,moyenne):
        print("Parametrage du capteur: ")
        if int(moyenne)  == 1: self.serial.write(b'\x81\x11\x6E') #1s
        if int(moyenne) == 10: self.serial.write(b'\x81\x12\x6D') #10s
        if int(moyenne) == 60: self.serial.write(b'\x81\x13\x6C') #60s
        else: print("Attention: changer la moyenne dans fichier de config.ini")
        time.sleep(0.36)
        response = self.serial.read(15)
        print("Reponse paramétrage: ",response)
        print("Parametrage nextPM: OK")
        time.sleep(1.1)
      
    def getMesures(self,moyenne):
        #Fonction pour lire les données du capteur
        if int(moyenne)  == 1: self.serial.write(b'\x81\x11\x6E') #1s
        if moyenne == 10: self.serial.write(b'\x81\x12\x6D') #10s
        if moyenne == 60: self.serial.write(b'\x81\x13\x6C') #60s
        time.sleep(0.36)
        byte = self.serial.read(size = 1)
        #print(datetime.now().strftime("%d %b %Y %H:%M:%S: "),byte)
        if byte == b'\x81':
            sentence = self.serial.read(size=15)
            #print(sentence)
            #print(len(sentence))
            #PM_1_pcs_ml = (sentence[3]*256+sentence[4])/1 #PM1 en nbre de particules par ml
            #PM_25_pcs_ml = (sentence[5]*256+sentence[6])/1 #PM1 en nbre de particules par ml
            #PM_10_pcs_ml = (sentence[7]*256+sentence[8])/1 #PM1 en nbre de particules par ml
            #res = "PM1: {} pcs/ml, PM2.5: {} pcs/ml, PM10: {} pcs/ml".format(PM_1_pcs_ml,PM_25_pcs_ml,PM_10_pcs_ml)
            #print(datetime.now().strftime("%d %b %Y %H:%M:%S : "),res)
            pm_1 = (sentence[9]+sentence[10])/10 #PM1 en microg par m3
            pm_25 = (sentence[11]+sentence[12])/10 #PM2.5 en microg par m3
            pm_10 = (sentence[13]+sentence[14])/10 #PM10 en microg par m3
            line = "PM1: {} µg/m3, PM2.5: {} μg/m3, PM10: {} μg/m3".format(pm_1,pm_25, pm_10)
            
            #print(datetime.datetime.now().strftime("%d %b %Y %H:%M:%S : "),line)
            return {"PM1": pm_1, "PM2.5":pm_25,"PM10":pm_10}
            
        else:
            print("Pas de données valides")
            PM1 =''
            PM25 = ''
            PM10 = ''
            #now = datetime.datetime.now()
            #nowD = now.strftime('%Y-%m-%d %H:%M:%S')
            return {"PM1":PM1,"PM2.5":PM25,"PM10":PM10}
        time.sleep(1)
            
########################################
        
#Corps du programme
test = NextPM()
test.parametrage(1)
while True:
    res = test.getMesures(sample)
    test.parametrage(1)