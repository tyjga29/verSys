from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import json
import time
import psutil

from data_handler import search_whole_table

server_number = 3

if server_number==1:
    address = 'SmartCityReceiver1'
    port_number = 9024
elif server_number==2:
    address = 'SmartCityReceiver2'
    port_number = 9024
elif server_number==3:
    address = 'SmartCityReceiver3'
    port_number = 9024

#port_number = int(os.environ.get("PORT_NUMBER"))

table = "air_quality"

# Caching variables
cache = {}
cache_expiry = 60000  # 60 seconds = 1 minute

class SmartCityReceiver(BaseHTTPRequestHandler):
    server_version = f"{address}/0.1"

    #HTTP Get Requests Server
    def do_GET(self):
        #Get current data
        if self.path == f'/{address}/getData':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            data = fetch_data(table)
        
            print(f"The data is {data}.")
            print(f"The data is from {cache[table]['timestamp_db']}.")
            print(f"Data newly retrieved at {cache[table]['timestamp_access']}.")
            print()
            json_data = json.dumps(data)
            json_bytes = json_data.encode('utf-8')
            self.wfile.write(json_data.encode('utf-8'))

        #Get Worload of System
        elif self.path == f'/{address}/getWorkload':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_percent_str = str(cpu_percent)
            self.wfile.write(cpu_percent_str.encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()
            message = "Not Found"
            self.wfile.write(bytes(message, "utf8"))

def run(server_class=HTTPServer, handler_class=SmartCityReceiver, port=port_number):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    
    print(f'Starting {handler_class.server_version} server on port {port}...')
    httpd.serve_forever()

def fetch_data(table):
    if table in cache and time.time() - cache[table]['timestamp_db'] < cache_expiry:
        print("Cached data.")
        print(f"{cache[table]['data']}")
        return cache[table]['data']
    else:
        print("Data has to be newly retrieved.")
        # Make HTTP request to fetch data
        result = search_whole_table(table)
        # Update cache with fetched data and timestamp
        timestamp = 0
        for entry in result:
            if 'timestamp' in entry:
                timestamp = entry['timestamp']
                entry["timestamp"] = datetime.fromtimestamp(entry["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
        current_time = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        cache[table] = {'data': {'result': result}, 'timestamp_db': timestamp, 'timestamp_access': current_time}
        return {'result': result}

if __name__ == '__main__':
    run()

