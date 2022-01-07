import configparser
import logging
import time
import csv

from duration_client import call_api_for_duration

logging.basicConfig(
	format='%(asctime)s %(message)s', 
	datefmt='%Y-%m-%dT%H:%M:%S%z',
	level=logging.INFO
	)

def main():
	api_key_config = configparser.ConfigParser()
	api_key_config.read('/Users/daniel/projects/commuter/conf/secrets/api_keys.conf')
	google_maps_api_key = api_key_config['api_keys']['google_maps_api_key']

	places = configparser.ConfigParser()
	places.read('/Users/daniel/projects/commuter/conf/secrets/places.conf')
	home = places['DEFAULT']['home']
	work = places['DEFAULT']['work']

	home_to_work_response = call_api_for_duration(
		origin = home, 
		destination = work, 
		api_key = google_maps_api_key
	)

	work_to_home_response = call_api_for_duration(
		origin = work, 
		destination = home, 
		api_key = google_maps_api_key
	)

	current_epoch_second = time.time()

	data = [
		[current_epoch_second, home, work, home_to_work_response.transit_duration_minutes],
		[current_epoch_second, work, home, work_to_home_response.transit_duration_minutes]
	]

	logging.info("Writing results to csv file")
	logging.info("Logging the data being written:")
	logging.info(data)
	with open('/Users/daniel/projects/commuter/output/data.csv','a+') as f:
		writer = csv.writer(f)
		writer.writerows(data)

if __name__ == '__main__':
	main()