import requests
import urllib.parse
import configparser
import logging
import time
from dataclasses import dataclass
from typing import Union

logging.basicConfig(
	format='%(asctime)s %(message)s', 
	datefmt='%Y-%m-%dT%H:%M:%S%z',
	level=logging.INFO
	)


@dataclass 
class ParsedApiResponse:
	status_code: int 
	transit_duration_minutes: int


def call_api_for_duration(origin: str, destination: str, api_key: str) -> Union[ParsedApiResponse, None]:
	"""
	Queries the google maps API to get the current duration, including traffic, from 
	origin to destination.

	params:
	origin: A place id representing the origin, used to robustly indicate a point on a map. 
	See e.g. https://developers.google.com/maps/documentation/places/web-service/place-id 
	destination: A place id representing the destination.
	api_key: The api key to access google maps platform

	returns: An ParsedApiResponse object containing the http response status code as well as 
	the duration of the trip in minutes, if the query was successful.
	"""
	base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
	params = {
		'origins' : f'place_id:{origin}',
		'destinations' : f'place_id:{destination}',
		'departure_time' : 'now',
		'key' : api_key
	}

	logging.info(f"Query google maps distance matrix api for duration from {origin} to {destination}")
	response = requests.get(base_url, params = params)
	response_content_json = response.json()
	response.close()

	if response.status_code == 200:
		try: 
			current_transit_duration_minutes = round(
				response_content_json['rows'][0]['elements'][0]['duration_in_traffic']['value'] / 60
				)
			logging.info("Successfully parsed the api response to get the duration.")
			return ParsedApiResponse(response.status_code, current_transit_duration_minutes)
		except Exception as e:
			logging.error(f'Failed with unexpected exception {e}!')

	else:
		logging.error(f"HTTP request failed with status code {response.status_code}")

		


def main():
	api_key_config = configparser.ConfigParser()
	api_key_config.read('/Users/daniel/projects/commuter/conf/secrets/api_keys.conf')

	places = configparser.ConfigParser()
	places.read('/Users/daniel/projects/commuter/conf/secrets/places.conf')

	parsed_api_response = call_api_for_duration(
		origin = places['DEFAULT']['home'],
		destination = places['DEFAULT']['work'],
		api_key = api_key_config['api_keys']['google_maps_api_key']
		)

	logging.info(f"Retrieved and parsed api response {parsed_api_response}")

if __name__ == '__main__':
	main()