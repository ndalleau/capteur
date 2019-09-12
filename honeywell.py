import serial
from datetime import datetime
import time

# Variables #################
DEFAULT_SERIAL_PORT = "/dev/ttyUSB1" # Serial port to use if no other specified ttyS0 si SDS011 branche sur uart du raspberry
sample = 10 #Variable de moyennage en secondes


# Constantes ###############
DEFAULT_BAUD_RATE = 9600 # Serial baud rate to use if no other specified
DEFAULT_SERIAL_TIMEOUT = 2 # Serial timeout to use if not specified
DEFAULT_READ_TIMEOUT = 1 #How long to sit looking for the correct character sequence.

MSG_CHAR_1 = b'\x42' # First character to be recieved in a valid packet
MSG_CHAR_2 = b'\x4d' # Second character to be recieved in a valid packet
############################


#Classes
class Honeywell:
    "Objet capteur Honeywell HPMA"
    def __init__(self,
                 port = DEFAULT_SERIAL_PORT,
                 baud=DEFAULT_BAUD_RATE,
                 serial_timeout = DEFAULT_SERIAL_TIMEOUT,
                 read_timeout = DEFAULT_READ_TIMEOUT):
        self.port = port
        self.baud = baud
        self.serial_timeout = serial_timeout
        self.read_timeout = read_timeout
        
        self.serial = serial.Serial(port=self.port,
                                    baudrate=self.baud,
                                    timeout=self.serial_timeout)
        
        
    def acquisition(self):
        "Acquisition données PM2.5 et PM10"
        #capteur = serial.Serial(self.port)
        byte = self.serial.read()
        #print(byte)
        if byte == MSG_CHAR_1:
            sentence = self.serial.read(size=31) # Read 31 more bytes
            #print ("Sentence size {}".format(len(sentence)))
            #print("sentence: ",sentence)
            PM25 = (sentence[6]+sentence[7])/1
            PM10 = (sentence[8]+sentence[10])/1
            line = "PM 2.5: {} μg/m^3  PM 10: {} μg/m^3".format(PM25, PM10)
            # ignoring the checksum and message tail
            print(datetime.now().strftime("%d %b %Y %H:%M:%S.%f: ")+line)
            return {"PM2.5":PM25,"PM10":PM10}
        
    def moyenne(self,sample):
        i=0
        PM25,PM10=0,0
        while i <= sample:
            res = self.acquisition()
            PM25 = res["PM2.5"] + PM25
            PM10 = res["PM10"] + PM10
            #print (i,pm_25,pm_10)
            i+=1
        print('\n')
        #print(datetime.now().strftime("%d %b %Y %H:%M:%S"))
        print(datetime.now().strftime("%d %b %Y %H:%M:%S"),"Moyenne : PM2.5 {} , PM10 {}".format(round(PM25/i,1),round(PM10/i,1)))
        print("----")
        return {"PM2.5":PM25/i,"PM10":PM10/i}
            
            
        

#Corps du programme
test = Honeywell()
while True:
    res = test.moyenne(sample)
    print(res)
