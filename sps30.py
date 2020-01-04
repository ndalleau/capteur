"""
    Library to read data from Sensirion SPS30 particulate matter sensor

    by
    Szymon Jakubiak
    Twitter: @SzymonJakubiak
    LinkedIn: https://pl.linkedin.com/in/szymon-jakubiak

    MIT License

    Copyright (c) 2018 Szymon Jakubiak
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

    Units for measurements:
        PM1, PM2.5, PM4 and PM10 are in ug/m^3, number concentrations are in #/cm^3
"""
import serial, struct, time
from datetime import datetime
from operator import invert
import numpy as np

class SPS30:
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(self.port, baudrate=115200, stopbits=1, parity="N",  timeout=2)
    
    def start(self):
        self.ser.write([0x7E, 0x00, 0x00, 0x02, 0x01, 0x03, 0xF9, 0x7E])
        
    def stop(self):
        self.ser.write([0x7E, 0x00, 0x01, 0x00, 0xFE, 0x7E])
    
    def read_values(self):
        self.ser.flushInput()
        # Ask for data
        self.ser.write([0x7E, 0x00, 0x03, 0x00, 0xFC, 0x7E])
        toRead = self.ser.inWaiting()
        # Wait for full response
        # (may be changed for looking for the stop byte 0x7E)
        while toRead < 47:
            toRead = self.ser.inWaiting()
            time.sleep(0.1)
        raw = self.ser.read(toRead)
        
        # Reverse byte-stuffing
        if b'\x7D\x5E' in raw:
            raw = raw.replace(b'\x7D\x5E', b'\x7E')
        if b'\x7D\x5D' in raw:
            raw = raw.replace(b'\x7D\x5D', b'\x7D')
        if b'\x7D\x31' in raw:
            raw = raw.replace(b'\x7D\x31', b'\x11')
        if b'\x7D\x33' in raw:
            raw = raw.replace(b'\x7D\x33', b'\x13')
        
        # Discard header and tail
        rawData = raw[5:-2]
        
        try:
            data = struct.unpack(">ffffffffff", rawData)
            data_json = {
                "tags":{
                        "sensor": "sensirion SPS30"},
                "fields":{
                        "PM1":round(data[0],3),
                        "PM2.5":round(data[1],3),
                        "PM4":round(data[2],3),
                        "PM10":round(data[3],3),
                        "0.3÷0.5":round(data[4],3),
                        "0.3÷1":round(data[5],3),
                        "0.3÷2.5":round(data[6],3),
                        "0.3÷4":round(data[7],3),
                        "0.3÷10":round(data[8],3),
                        "typical size":round(data[9],3)}}
            print(datetime.now().strftime("%d %b %Y %H:%M:%S"),' : ',data_json)
            print("\n")
            time.sleep(1)
            return data_json
        except struct.error:
            data = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

                
    def moyenne(self,sample):
        i=0
        PM1list= list()
        PM25list = list()
        PM4list = list()
        PM10list = list()
        while i<=sample:
            res = self.read_values()
            if res["fields"]["PM1"] !='': PM1list.append(res["fields"]["PM1"])
            if res["fields"]["PM2.5"] !='': PM25list.append(res["fields"]["PM2.5"])
            if res["fields"]["PM4"] !='': PM4list.append(res["fields"]["PM4"])
            if res["fields"]["PM10"] !='': PM10list.append(res["fields"]["PM10"])
            i+=1
        PM1res = np.array(PM1list) #Moyenne PM1
        PM1mean = PM1res.mean()
        PM25res = np.array(PM25list)
        PM25mean = PM25res.mean()  #Moyenne PM25
        PM4res = np.array(PM4list)
        PM4mean = PM4res.mean() #Moyenne PM4
        PM10res = np.array(PM10list)
        PM10mean = PM10res.mean()  #Moyenne PM10
        print('\n')
        print("----")
        print("{}: Moyenne : PM1 {}, PM2.5 {} , PM4 {}, PM10 {}".format(datetime.now().strftime("%d %b %Y %H:%M:%S"),round(PM1mean,3),round(PM25mean,3),round(PM4mean,3),round(PM10mean,3)))
        print("----")
        print('\n')
        return {
                "tags":{
                    "sensor": "honeywell"},
                "fields":{
                    "PM1":round(PM1mean,2) ,  
                    "PM2.5":round(PM25mean,2),
                    "PM4":round(PM4mean,2),
                    "PM10":round(PM10mean,2)}
                    }
    
    def read_serial_number(self):
        self.ser.flushInput()
        self.ser.write([0x7E, 0x00, 0xD0, 0x01, 0x03, 0x2B, 0x7E])
        toRead = self.ser.inWaiting()
        while toRead < 24:
            toRead = self.ser.inWaiting()
            time.sleep(0.1)
        raw = self.ser.read(toRead)
        
        # Reverse byte-stuffing
        if b'\x7D\x5E' in raw:
            raw = raw.replace(b'\x7D\x5E', b'\x7E')
        if b'\x7D\x5D' in raw:
            raw = raw.replace(b'\x7D\x5D', b'\x7D')
        if b'\x7D\x31' in raw:
            raw = raw.replace(b'\x7D\x31', b'\x11')
        if b'\x7D\x33' in raw:
            raw = raw.replace(b'\x7D\x33', b'\x13')
        
        # Discard header, tail and decode
        serial_number = raw[5:-3].decode('ascii')
        return serial_number

    def close_port(self):
        self.ser.close()
