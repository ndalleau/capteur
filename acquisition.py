# Parseur ############################################################################
#Le parseur definit les paramètres à compléter lors du lancement du script
#Dans le cadre de ce script il s'agit uniquement du fichier de configuration fichier.ini
description="""fichier de configuration, par defaut config.ini"""
parseur=argparse.ArgumentParser(description=description)
parseur.add_argument('-c','--config',dest='config',default='config.ini',help='fichier de configuration',type=str)

args = parseur.parse_args()
######################################################################################

# Lecture du fichier de configuration.ini ############################################
parser = configparser.ConfigParser()
parser.read(args.config)

######################################################################################


#Variables #########################
DEFAULT_SERIAL_PORT = "/dev/ttyUSB0"
moyenne = 10


import SDS011
capteur = SDS011.SDS011(port = DEFAULT_SERIAL_PORT)

while True:
    res  = capteur.moyenne(moyenne)






