from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
import requests
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

servers = [
    "SmartCityReceiver1",
    "SmartCityReceiver2",
    #"SmartCityReceiver3"
]
ports= [
    '8080',
    "8081",
    #8082
]
#port = int(os.environ.get("PORT_NUMBER"))

current_server_index = 0
def get_next_server():
    global current_server_index
    server = servers[current_server_index]
    current_server_index = (current_server_index + 1) % len(servers)
    return server

current_port_index = 0
def get_next_port():
    global current_port_index
    port = ports[current_port_index]
    current_port_index = (current_port_index + 1) % len(ports)
    return port

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.get("/search_whole")
async def search_whole():
    for _ in range(len(servers)):
        server = get_next_server()
        port = get_next_port()
        url = f"http://localhost:{port}/{server}/getData"
        print(f"Sending Get Request to {url}")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Response received successfully from server {server}:")
                print("Response ", response.text)
                parsed_data = response.json()
                return parsed_data
            else:
                print(f"Failed to retrieve data from {server}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data from {server}: {e}")
    return {"error": "Failed to retrieve data from all servers."}
