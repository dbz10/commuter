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
	secrets_conf = configparser.ConfigParser()
	secrets_conf.read('/Users/daniel/projects/commuter/conf/secrets/secrets.conf')
	
	google_maps_api_key = secrets_conf['api_keys']['google_maps_api_key']
	home = secrets_conf['places']['home']
	work = secrets_conf['places']['work']

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