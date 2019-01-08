import requests
from orvibo.orvibo import Orvibo
from datetime import datetime, timedelta
import time
from dateutil import tz

def getSunsetTime():
    url = "https://api.sunrise-sunset.org/json"
    parameters = {'lat' : '38.8812903', 'lng': '-77.3948165'}
    r = requests.get(url, params=parameters).json()
    return r['results']['sunset']

def toggleSwitches():
    for args in Orvibo.discover().values():
        device = Orvibo(*args)
        device.on = not device.on

def convertToScheduleTime(utcSunsetTime):
    fromZone = tz.tzutc()
    toZone = tz.tzlocal()
    datetimeSunsetUtc = datetime.strptime(utcSunsetTime, '%I:%M:%S %p')
    datetimeSunsetUtc = datetimeSunsetUtc.replace(tzinfo=fromZone)
    return datetimeSunsetUtc.astimezone(toZone) - timedelta(minutes=30)


if __name__=="__main__":

    print("Started Sunset Timer")
    sunsetTimeString = getSunsetTime()
    sunsetTime = convertToScheduleTime(sunsetTimeString)

    while True:
        currentTime = datetime.now()
        # Run once everyday at noon to get sunset time
        if (currentTime.hour * 100 + currentTime.minute) == 1200:
            sunsetTimeString = getSunsetTime()
            sunsetTime = convertToScheduleTime(sunsetTimeString)

        if currentTime.hour == sunsetTime.hour and currentTime.minute == sunsetTime.minute:
            toggleSwitches()

        time.sleep(30)