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


# Lecture des variables issues du fichier de config ##################################
portCom = '/dev/'+ parser['CAPTEUR']['port']
sensor = parser['CAPTEUR']['sensor']

moyenne = parser['MESURE']['moyenne'] #duree moyennage en secondes dans le fichier de configuration
site = parser['MESURE']['site'] #site de mesure dans le fichier de configuration

######################################################################################



if sensor == 'sds011':
    import SDS011
    capteur = SDS011.SDS011(port = portCom)
    
elif sensor == 'honeywell':
    import honeywell
    capteur = honeywell.Honeywell(port = portCom)

while True:
    res  = capteur.moyenne(moyenne)






