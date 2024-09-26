from elasticsearch import Elasticsearch

#Step 1: initializing the ElasticSearch Client
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

#Step 2: defining the index name
index_name = "esflight"

#Step 3: defining the mapping for the index
mapping = {
    "mappings": {
        "properties": {
         "position":{"type":"geo_point"},
         "hex": { "type": "keyword" },
         "reg_number":{"type": "keyword"},
         "flag":{"type":"keyword"},
         "alt":{"type":"float"},
         "dir":{"type":"float"},
         "speed":{"type":"integer"},
         "v_speed":{"type":"integer"},
         "flight_number":{"type":"keyword"},
         "flight_iata":{"type":"keyword"},
         "dep_iata":{"type":"keyword"},
         "arr_iata":{"type":"keyword"},
         "airline_iata":{"type":"keyword"},
         "aircraft_icao": { "type": "keyword" },
         "status": { "type": "keyword" },
         "type": { "type": "keyword" },
         "arr_pos":{"type":"geo_point"},
         "dep_pos":{"type":"geo_point"},
         "Departure":{"type":"keyword"},
         "Arrival":{"type":"keyword"},
         }
    }
}

#Step 4
#if the airplane changes position it will be deleted and updated to the new one
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    print(f"Index '{index_name}' has been deleted.")
else:
    print(f"Index '{index_name}' does not exist.")

#Step 5: creating the ELK index
es.indices.create(index=index_name, body=mapping)