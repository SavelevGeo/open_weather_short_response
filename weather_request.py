import requests
import pandas as pd

def req(coords, test = True):
    if test:
        return '14 13-18-17-12,804,0 13-15-16-11,500,53 11-18-18-15,803,0 13-20-19-16,801,0 14-24-24-20,803,0 17-25-26-21,801,0 20-26-25-23,804,13 21-30-28-24,803,0'
    else:
        #daily
        #coords = '59.94882271675465, 30.30343904190325'
        key = 'd96c1e8e1e406107036f796bfd2c2669'
        lat, lon = coords.split(', ')
        response = requests.get(
                    f'https://api.openweathermap.org'
                    + f'/data/2.5/onecall?'
                    + f'lat={lat}&lon={lon}'
                    + f'&units=metric'
                    + f'&lang=ru'
                    + f'&exclude=minutely'
                    + f'&appid={key}'
                    ).json()
        off = response['timezone_offset']
        dailyDf = pd.DataFrame(response['daily'])
        days = pd.to_datetime(dailyDf.dt+off, unit='s').astype(str)
        day_num = days.str.split(pat='[- ]', expand=True)[2]
        tmp = dailyDf.temp.apply(
                    lambda t: '-'.join(
                                    [str(round(dp)) for dp in
                                    [t['morn'], t['day'], t['eve'], t['night']]]
                                    )
                    )
        wdsc = dailyDf.weather.apply(lambda w: w[0]['description'])
        pop = pd.Series(dailyDf['pop'].values * 100).astype(int).astype(str) + '%'
        outDf = pd.DataFrame(
                            [
                            day_num,
                            tmp,
                            wdsc,
                            pop,
                            ]
                            ).T
        outDf.columns = ['day', 'temp', 'weather', 'pop']
        outDf.index = outDf.day

        #hourly
        hourlyDf = pd.DataFrame(response['hourly'])
        time = pd.to_datetime(hourlyDf.dt+off, unit='s').astype(str)
        day_hour = time.str.split(pat='[- :]', expand=True).iloc[:,2:4]
        pop = pd.Series(hourlyDf['pop'].values * 100).astype(int).astype(str) + '%'
        dh = day_hour[2] + ' ' + day_hour[3] + ' ' + pop

        return outDf.drop(columns=['day']), dh.tolist()

