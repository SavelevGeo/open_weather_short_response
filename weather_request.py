import requests
import pandas as pd

def req(coords, test = True):
	if test:
		outText = '14 13-18-17-12,804,0 13-15-16-11,500,53 11-18-18-15,803,0 13-20-19-16,801,0 14-24-24-20,803,0 17-25-26-21,801,0 20-26-25-23,804,13 21-30-28-24,803,0'
	else:
		key = 'd96c1e8e1e406107036f796bfd2c2669'
		lat, lon = coords.split(', ')
		response = requests.get(
					f'https://api.openweathermap.org'
					+ f'/data/2.5/onecall?'
					+ f'lat={lat}&lon={lon}'
					+ f'&units=metric'
					+ f'&lang=ru'
					+ f'&exclude=hourly,minutely'
					+ f'&appid={key}'
					).json()

		dt = response['current']['dt']
		off = response['timezone_offset']
		result_s=pd.to_datetime(dt+off,unit='s')
		start = int(
			   str(result_s).split()[0].split('-')[2]
			   )
		
		off = response['timezone_offset']
		dailyDf = pd.DataFrame(response['daily'])
		
		tmp = dailyDf.temp.apply(
					lambda t:
					   '-'.join(
							   [str(round(dp))
							    for dp in
							     [
							      t['morn'], 
							      t['day'], 
							      t['eve'], 
							      t['night'] 
							     ]
							   ]
							   )
					)
		
		wid = dailyDf.weather.apply(lambda w: w[0]['id'])
		
		pop = dailyDf['pop'].values*100
		pop = pop.astype(int)
		
		outDf = pd.DataFrame(
				     [
				      tmp,
				      wid,
				      pop,
				     ]
				    ).T
		
		outText = ' '.join(
				   [
				   str(start),
				   outDf.to_csv(
						sep = ',',
						header = None,
						index = None, 
						line_terminator = ' ' 
					   	)
				   ]
				  )
	return outText
	

