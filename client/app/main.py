from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
import requests
import time

app = FastAPI()
templates = Jinja2Templates(directory="templates")

cpu_workload_threshold = 70.0

theo_servers = [
    "SmartCityReceiver1",
    "SmartCityReceiver2",
    "SmartCityReceiver3"
]
theo_ips= [
    '192.168.180.65',
    '192.168.180.66',
    '192.168.180.67'
]
servers = []
ips = []

#port = int(os.environ.get("PORT_NUMBER"))

current_server_index = 0
def get_next_server():
    global current_server_index
    server = servers[current_server_index]
    current_server_index = (current_server_index + 1) % len(servers)
    return server

current_ip_index = 0
def get_next_ip():
    global current_ip_index
    ip = ips[current_ip_index]
    current_ip_index = (current_ip_index + 1) % len(ips)
    return ip

overload = False
def arrange_arrays():
    global overload, theo_ips, theo_servers, ips, servers
    overload = False
    print("Checking status of CPU's.")
    for i in range(len(theo_servers)):
        cpu_workload = get_cpu_workload(theo_servers[i], theo_ips[i])
        if cpu_workload is not None and cpu_workload <= cpu_workload_threshold:
            print(f"CPU Workload of {theo_servers[i]} on ip {theo_ips[i]} is: {cpu_workload}%.")
            print("This is acceptable.")
            servers.append(theo_servers[i])
            ips.append(theo_ips[i])
        elif cpu_workload is None:
            print(f"No response received from server {theo_servers[i]} on ip {theo_ips[i]}. Skipping...")
        else:
            print(f"CPU Workload of {theo_servers[i]} on ip {theo_ips[i]} is: {cpu_workload}%.")
            print("This exceeds the threshold. Skipping...")

    if not servers and not ips:
        overload = True

def get_cpu_workload(server, ip):
    url = f"{ip}:9024/{server}/getWorkload"
    print(f"Sending Get Request to {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Response received successfully from server {server}:")
            print("Response ", response.text)
            return float(response.text)
        else:
            print(f"Failed to retrieve data from. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data from: {e}")
        return None

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

last_server_update = None
duration_update_servers = 60 #60 seconds
@app.get("/search_whole")
async def search_whole():
    global last_server_update, duration_update_servers, overload, servers
    print()
    if (last_server_update is not None):
        time_gap = time.time() - last_server_update
        print(f"Time since last inspeciton of the servers: {time_gap}")

    # Check if overload is true at the beginning
    if overload:
        print("Server overload detected. Retrying...")
        arrange_arrays()
        last_server_update = time.time()
        return await search_whole()  # Retry the function
    
    #Check if it the first time or if it is time to rearrange the servers
    if len(servers) == 0 or time_gap >= duration_update_servers:
        arrange_arrays()
        last_server_update = time.time()

    for _ in range(len(servers)):
        server = get_next_server()
        ip = get_next_ip()
        url = f"{ip}:9024/{server}/getData"
        print(f"Sending Get Request to {url}")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print()
                print(f"Response received successfully from server {server}:")
                print("Response ", response.text)
                parsed_data = response.json()
                return parsed_data
            else:
                print(f"Failed to retrieve data from {server}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data from {server}: {e}")
    return {"error": "Failed to retrieve data from all servers."}

