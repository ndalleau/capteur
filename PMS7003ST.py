import serial

port = '/dev/ttyS0'
baudRate = 9600

MSG_CHAR_1 = b'\x42' # First character to be recieved in a valid packet
MSG_CHAR_2 = b'\x00' # Second character to be recieved in a valid packet
nByte = 31

capteur = serial.Serial(port,baudrate = 9600,timeout=1)

while True:
    byte1 = capteur.read(size = 1)
    #print("byte 1: ",byte1)
    if byte1 == MSG_CHAR_1:
        datas = capteur.read(size = 39)
        print(datas)
        print('\n======= PMS5003ST ========\n'
              'PM1.0(CF=1): {}\n'
              'PM2.5(CF=1): {}\n'
              'PM10 (CF=1): {}\n'
              'PM1.0 (STD): {}\n'
              'PM2.5 (STD): {}\n'
              'PM10  (STD): {}\n'
              '>0.3um     : {}\n'
              '>0.5um     : {}\n'
              '>1.0um     : {}\n'
              '>2.5um     : {}\n'
              '>5.0um     : {}\n'
              '>10um      : {}\n'
              'HCHO       : {}\n'
              'temperature: {}\n'
              'humidity(%): {}'.format(datas[4]+datas[5],
                                       datas[6]+datas[7],
                                       datas[8]+datas[9],
                                       datas[10]+datas[11], #PM1
                                       datas[12]+datas[13],
                                       datas[14]+datas[15],
                                       datas[16]+datas[17],
                                       datas[18]+datas[19],
                                       datas[20]+datas[21],
                                       datas[22]+datas[23],
                                       datas[24]+datas[25],
                                       datas[26]+datas[27],
                                       (datas[28]+datas[29])/1000.0,
                                       (datas[30]+datas[31])/10.0,
                                       (datas[32]+datas[33])/10.0))
