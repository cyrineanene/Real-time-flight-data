#This producer will get the data from the AirLabs API and store it into a Kafka Producer

import requests
from kafka import KafkaProducer
import json
import time
from datetime import datetime
import os

#Step1: Configure AirLabs API
API_KEY = 'AIRLABS_API_KEY'
base_url = 'https://airlabs.co/api/v9/flights'

#Step2: Create and configure a Kafka Producer
bootstrap_servers = 'localhost:9092'
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers, 
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
flight_topic = "flight"

#Step3: Fetch the Data
while True:
    try:
        url = f"{base_url}?api_key={API_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()['response']

            #Step 4: Send the Processed Data to Kafka 
            for line in data:
                    #creating a directory for each line of data
                    position = {
                        'lat': line.get('lat'),
                        'lon': line.get('lng'),
                    }
                    d = {
                        "hex": line.get('hex'),
                        "reg_number": line.get('reg_number'),
                        "flag": line.get('flag'),
                        "position": position,
                        'alt': line.get('alt'),
                        'dir': line.get('dir'),
                        "speed": line.get('speed'),
                        "v_speed": line.get('v_speed'),
                        "flight_number": line.get('flight_number'),
                        "flight_icao": line.get('flight_icao'),
                        "flight_iata": line.get('flight_iata'),
                        "dep_icao": line.get('dep_icao'),
                        "dep_iata": line.get('dep_iata'),
                        "arr_icao": line.get('arr_icao'),
                        "arr_iata": line.get('arr_iata'),
                        "airline_icao": line.get('airline_icao'),
                        "airline_iata": line.get('airline_iata'),
                        "aircraft_icao": line.get('aircraft_icao'),
                        "updated": line.get('updated'),
                        "status": line.get('status')
                    }

                    #sending the directory to the producer
                    producer.send('flight', value=d)
                    #print(d)

                    #A delay of 0.05sec not to overload the producer/broker
                    time.sleep(0.05)

    except Exception as e:
        print(f'An error occurred: {str(e)}')

    #a delay of 60sec between each line of data 
    time.sleep(60) 