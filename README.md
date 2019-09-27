# capteur
Ce script permet:
* Acquisition de données issues de différents microcapteurs de mesures des particules en suspension (SDS011, honeywell, plantower, etc...)
* Stockage des résultats dans une base InfluxDB et/ou un fichier texte
* Envoi des résultats vers le site Luftdaten.info (affichage sur la carte du site)


# Branchement des capteurs PM
Les capteurs sont branchés sur les ports USB en utilisant un module FTDI


# Exécution du script

Pour éxécuter le script: 
python acquisition.py -c config.ini

config.ini est un fichier de configuration qui définit les différents paramètres nécessaires au bon fonctionnement du script:
* Port sur lequel est branché le capteur: exemple ttyUSB0
* Sensor définit le modèle de sensor qui est branché
