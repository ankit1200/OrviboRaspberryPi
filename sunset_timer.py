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
    datetimeSunsetUtc = datetimeSunsetUtc.replace(year=2019, tzinfo=fromZone)
    return datetimeSunsetUtc.astimezone(toZone) - timedelta(minutes=30)


if __name__=="__main__":

    print("Started Sunset Timer")
    sunsetTimeString = getSunsetTime()
    sunsetTime = convertToScheduleTime(sunsetTimeString)

    while True:
        currentTime = datetime.now()
        print("Current Time: " +  str(currentTime))
        # Run once everyday at noon to get sunset time
        if (currentTime.hour * 100 + currentTime.minute) == 1200:
            try:
                sunsetTimeString = getSunsetTime()
                sunsetTime = convertToScheduleTime(sunsetTimeString)
                print("Sunset Time: " + str(sunsetTime))
            except Exception as e:
                print("ERROR OCCURED GETTING SUNSET TIMES: " + str(e))

        if (sunsetTime.hour < 7 and currentTime.hour == sunsetTime.hour and currentTime.minute == sunsetTime.minute):
            toggleSwitches()
        elif currentTime.hour == 19 and currentTime.minute == 0:
            toggleSwitches()

        time.sleep(60)
