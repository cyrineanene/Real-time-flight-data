#this code will enable to connect to Kibana and load the ndjson, the template to the interface

. /opt/bitnami/scripts/liblog.sh

# Function to check if Kibana is ready
check_kibana_ready() {
    until curl -s http://kibana-cntr:5601; do
        echo "Waiting for Kibana..."
        sleep 3
    done
    echo "Kibana is ready."
}

# Function to import saved objects
import_saved_objects() {
    local file_path="$1"
    local response=$(curl -s -X POST localhost:5601/api/saved_objects/_import -H "kbn-xsrf: true" --form file=@"$file_path")
    echo "$response"
}

# Path to the export NDJSON file
export_ndjson_file="/usr/share/kibana/scripts/export.ndjson"

# Check if Kibana is ready
check_kibana_ready

# Import the saved objects
import_saved_objects "$export_ndjson_file"