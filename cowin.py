#!/usr/bin/python3
import aiohttp
import asyncio
import json
import user
import datetime
import time



sema = asyncio.BoundedSemaphore(5)
def logger(message):
	t1 = datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S:%f %p')
	log = f'{t1} :{message}'
	file = open('run_log.log', 'a')
	file.write(log+'\n')
	file.close()

async def getPage(URL):
	headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"}
	try: 
		async with aiohttp.ClientSession(headers=headers,trust_env=True) as session:
			async with sema,session.get(URL) as response:
				source = await response.read( )
				
				result_dict = json.loads(source)
				return result_dict
	except asyncio.CancelledError:
		logger(f'Error retrieving json for url:{URL}')

async def getDetails(URL):
	result_dict = await getPage(URL)
	all_centers = result_dict.get('centers', [])
	dose_available = {}
	for center in all_centers:
		sessions = list(filter(lambda x: x['available_capacity_dose1']!=0, center['sessions']))
		if sessions:
			dose_available[center['name']] = sum([x['available_capacity_dose1'] for x in sessions])
			# dose_available[center['center_id']] = sum([x['available_capacity_dose1'] for x in sessions])
	return dose_available

async def main():
	pincodes = [682305, 682314, 682312 ]
	usr_1 = user.user(pincodes)
	pincode_availability = {}
	while True:
		for x in range(15):
			v_date=(datetime.datetime.now()+datetime.timedelta(days=x)).strftime('%d-%m-%Y')
			urls = [f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={v_date}' for pincode in pincodes]
			dose_available = await asyncio.gather(*[getDetails(link) for link in urls])
			for x in range(len(pincodes)):
				if not pincode_availability.get(pincodes[x], False) and dose_available[x]:
					pincode_availability[pincodes[x]] = dose_available[x]
		usr_1.notify(pincode_availability)
		time.sleep(60)


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
