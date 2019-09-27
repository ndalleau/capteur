# capteur

Acquisition de données issues de microcapteurs de mesures des particules en suspension (SDS011, honeywell, plantower, etc...)
Stockage des résultats dans une base InfluxDB
Envoi des résultats vers le site Luftdaten


# Branchement des capteurs PM
Les capteurs sont branchés sur les ports USB en utilisant un module FTDI


# Exécution du script

Pour éxécuter le script: 
python acquisition.py -c config.ini

config.ini définit les différents paramètres:
* Port sur lequel est branché le capteur: exemple ttyUSB0
* Sensor définit le modèle de sensor qui est branché
