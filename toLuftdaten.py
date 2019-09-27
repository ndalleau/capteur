# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 14:47:05 2019

@author: ndalleau

Module pour exporter les données issues des microcapteurs vers le site de Luftdaten.info

"""

def pushLuftdaten(res):
    #Fonction pour envoyer des mesures de particules PM2.5 et PM10 sur la carte Luftdaten
    urlLuftdaten = 'https://api.luftdaten.info/v1/push-sensor-data/'
    values = {"P1": res["fields"]["PM10"],
              "P2": res["fields"]["PM2.5"]}
    sensordatavalues = [{"value_type": key, "value": val} for key, val in values.items()]
    data = {"software_version": "ATMO_AuRA", 
        "sensordatavalues":sensordatavalues}
    headers = {"X-PIN":"1",
               "X-Sensor":res['tags']['Id_rasp']}
    rep = requests.post(urlLuftdaten,json=data,headers=headers)
    print(rep.text)
    return rep
