#As the API of AirLabs is no longer public, we can use the csv file instead of the API
#This has the same function as the kafka_producer.py script 

from kafka import KafkaProducer
import csv
import time
import json


#function to read csv file
def read_csv(file_path):
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

#flight Schema 
flight_schema = {
            "hex":int,
            "reg_number": str,
            "flag": str,
            "lat": float,
            "lng": float,
            "alt": float,
            "dir": float,
            "speed": int,
            "flight_number":int,
            "flight_icao": str,
            "flight_iata": str,
            "dep_icao": str,
            "dep_iata": str,
            "arr_icao":str ,
            "arr_iata":str ,
            "airline_icao": str,
            "airline_iata": str,
            "aircraft_icao": str,
            "status": str,
}

if __name__ == "__main__":

    #Step1: configure Kafka Producer
    bootstrap_servers = 'localhost:9093' 
    books_topic = "flight"
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers, 
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    
    #Step2: read csv file using read_csv function
    books_data = read_csv('data/flight_data.csv')
    
    #Step3: Send data to Kafka topic
    for line in books_data:
        flight_data_dict = {}
        for key, value in flight_schema.items():
             raw_value = line[key]
             if raw_value != '' :
                flight_data_dict[key] = value(raw_value)
             else:
                flight_data_dict[key] = None
        producer.send(books_topic, value=flight_data_dict)
        #print(f"Sent message to {books_topic}: {flight_data_dict}")
        time.sleep(1)

    #Step4: Close the producer
    producer.flush()
    producer.close()