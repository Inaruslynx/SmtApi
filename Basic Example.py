from SmtApi import SmtApi
import datetime
import json  # loading json file with username, password, and esiid


def main():
    pathlogin = "/log-in.json"
    pathcert = "/code.cert"
    pathkey = "/code.key"
    startDate = datetime.datetime(2021, 1, 18)
    endDate = datetime.datetime(2021, 1, 19)
   # data = {}
    with open(pathlogin) as f:
        data = json.load(f)
    example = SmtApi(data['user'], data['pass'],
                     (pathcert, pathkey), data['esiid'], Test=True)
    powerData = example.min_interval_reads(startDate,endDate)
    for index, day in enumerate(powerData):
        print("day:", day[index])
    pass


if __name__ == "__main__":
    main()
