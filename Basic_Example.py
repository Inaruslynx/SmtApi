from SmtApi import SmtApi
import datetime
import json  # loading json file with username, password, and esiid


def main():
    pathlogin = "/log-in.json"
    pathcert = "/code.cert"
    pathkey = "/code.key"
    # Never use today
    startDate = datetime.datetime(2021, 1, 18)
    endDate = datetime.datetime(2021, 1, 19)
   # data = {}
    with open(pathlogin) as f:
        data = json.load(f)
    # Note order of pathcert and pathkey and if not testing, leave off Test=True
    example = SmtApi(data['user'], data['pass'],
                     (pathcert, pathkey), data['esiid'], Test=True)
    # Methods will mostly work with just startDate and endDate, but it is possible to add more paramaters
    powerData = example.min_interval_reads(startDate, endDate)
    # days are a str and power usage will be a list of floats
    dates = powerData.keys()
    for day in dates:
        print("day:", day)
        print("power usage every 15 minutes:", powerData[day])
    # Next example is of daily reads
    dailyPowerData = example.daily_reads(startDate,endDate)
    dailyDates = dailyPowerData.keys()
    for day in dailyDates:
        print('day:', day)
        print('power used this day:', dailyPowerData[day])


if __name__ == "__main__":
    main()
