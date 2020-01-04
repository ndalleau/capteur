import configparser  #Module pour gérer l import d un fichier de configuration
import argparse #Module pour ajouter des paramètres lors de l appel du script 
from influxdb import InfluxDBClient  #Module pour gérer l export des données vers la base InfluxDB
import os
import sys
import toLuftdaten  #Module pour gérer l envoi des données vers le site luftdaten.info

# Parseur ############################################################################
#Le parseur definit les paramètres à compléter lors du lancement du script
#Dans le cadre de ce script il s'agit uniquement du fichier de configuration (par défaut config.ini)
description="""fichier de configuration, par defaut config.ini"""
parseur=argparse.ArgumentParser(description=description)
parseur.add_argument('-c','--config',dest='config',default='config.ini',help='fichier de configuration',type=str)

args = parseur.parse_args()
######################################################################################

# Lecture du fichier de configuration.ini ############################################
parser = configparser.ConfigParser()
parser.read(args.config)

#Variables issues du fichier de configuration.ini
DEFAULT_SERIAL_PORT = '/dev/'+ parser['CAPTEUR']['port']  #Port sur lequel est branche le sensor
sensor = parser['CAPTEUR']['sensor']
print('Capteur: ',sensor)

site = parser['MESURE']['site']
moyenne = int(parser['MESURE']['moyenne'])

measurement = parser['INFLUXDB']['measurement']

#######################################################################################

# Gestion csv ########################################################################
ficData = parser['EXPORT_CSV']['file_name']
csv = int(parser['EXPORT_CSV']['export']) #Mettre 1 dans fichier de config pour permettre ecriture des données dans un fichier csv
#######################################################################################

# Gestion InfluxDB ####################################################################
infl = int(parser['INFLUXDB']['export'])
clientInflux = InfluxDBClient(host = parser['INFLUXDB']['serveur'],
                        port = parser['INFLUXDB']['port'],
                        username = parser['INFLUXDB']['username'],
                        password = parser['INFLUXDB']['password'],
                        database = parser['INFLUXDB']['database'])
#######################################################################################

# extracts serial from cpuinfo ################################
#Extraire le numéro du Raspberry pour envoyer avec les données
def getSerial():
    """Fonction pour récupérer le numéro de série du raspberry"""
    with open('/proc/cpuinfo','r') as f:
        for line in f:
            if line[0:6]=='Serial':
                return(line[10:26])
    f.close()
    raise Exception('CPU serial not found')

raspId = getSerial()
###############################################################

print('\n')    
print('Lecture fichier de configuration: ',args.config)
print('\n')

#Verification de la presence d un capteur sur port:
if parser['CAPTEUR']['port'] not in os.listdir('/dev'):
    print("Attention pas de capteur detecté sur {0}".format(parser['CAPTEUR']['port']))
    sys.exit()
else:
    print("Capteur {0} sur port {1}".format(sensor, parser['CAPTEUR']['port']))
    
print("site de mesure: {0}".format(site))
print("Latitude: {0}, Longitude: {1}".format(parser['MESURE']['latitude'],parser['MESURE']['longitude']))
print("Moyenne en secondes: {0}".format(parser['MESURE']['moyenne']))
print('---')
print('\n')

#Export des données vers la base InfluxDB
print("Export des données vers InfluxDB {0}".format(parser['INFLUXDB']['export']))
print('Ecriture dans la base InfluxDB, server:{0}, database: {1}'.format(parser['INFLUXDB']['serveur'],parser['INFLUXDB']['database']))  
print('\n')

#Export des données vers le site luftdaten.info
if int(parser['LUFTDATEN']['export']) == 1:
    print("Export des données vers le serveur de luftdaten.info: OK")
else:
    print("Pas d export des données vers le site luftdaten.info") 
print('\n')

print("Id du raspberry: ",raspId)
print('\n')
print('---')

if sensor == 'SDS011':
    import SDS011
    capteur = SDS011.SDS011(port = DEFAULT_SERIAL_PORT) #Creation de l objet SDS011 sur port
    
elif sensor == 'honeywell':
    import honeywell
    capteur = honeywell.Honeywell(port = DEFAULT_SERIAL_PORT) #Creation de l objet Honeywell sur port
elif sensor == 'sps30':
    import sps30
    capteur = sps30.SPS30(port = DEFAULT_SERIAL_PORT) #Cration de l objet sensirion SPS30 sur port
else:
    print("Attention: Capteur inconnu")

# Se repete indefiniment
print("Debut des mesures: ")
while True:
        res  = capteur.moyenne(moyenne)
        res["tags"]["Id_rasp"]= raspId
        res["tags"]["port"] = DEFAULT_SERIAL_PORT
        res["tags"]["site"] = site
        res["measurement"] = measurement
        print([res])
        #Insertion de res dans la base InfluxDB
        if infl == 1: clientInflux.write_points([res])
        #Envoi des résultats vers site luftdaten.info
        if parser['LUFTDATEN']['export'] == 1: toLuftdaten(res)
    
    





