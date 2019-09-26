# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 14:47:05 2019

@author: ndalleau

Module pour exporter les données issues des microcapteurs vers le site de Luftdaten.info

"""

import requests

Id_rasp = "raspi-"+'00000000b5e4427b'

res = {"tags": {"Id_rasp":Id_rasp},
       "fields":
           {"PM10":15,
            "PM2.5":10}}

def sendLuftdaten(res):
    """pushLuftdaten('https://api-rrd.madavi.de/data.php', 0, {
        "SDS_P1":             res["fields"]["PM10"],
        "SDS_P2":             res["fields"]["PM2.5"],
        "BME280_temperature": res["fields"]["temperature"],
        "BME280_pressure":    res["fields"]["pressure"],
        "BME280_humidity":    res["fields"]["humidity"],
    })"""
    pushLuftdaten('https://api.luftdaten.info/v1/push-sensor-data/', 1, {
        "P1": res["fields"]["PM10"],
        "P2": res["fields"]["PM2.5"],
    })
    """pushLuftdaten('https://api.luftdaten.info/v1/push-sensor-data/', 11, {
        "temperature": res["fields"]["temperature"],
        "pressure":    res["fields"]["pressure"],
        "humidity":    res["fields"]["humidity"],
    })"""


def pushLuftdaten(url, pin, values):
    requests.post(url,
        json={
            "software_version": "python-dusty 0.0.1",
            "sensordatavalues": [{"value_type": key, "value": val} for key, val in values.items()],
        },
        headers={
            "X-PIN":    str(pin),
            "X-Sensor": Id_rasp,
        }
    )


print(res)
print(res["fields"]["PM10"])
print(res["fields"]["PM2.5"])

#Envoi des données à Luftdaten:
sendLuftdaten(res)
