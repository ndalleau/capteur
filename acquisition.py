import SDS011

#Variables #########################
DEFAULT_SERIAL_PORT = "/dev/ttyUSB0"
moyenne = 10



capteur = SDS011.SDS011(port = DEFAULT_SERIAL_PORT)

while True:
    res  = capteur.moyenne(moyenne)






