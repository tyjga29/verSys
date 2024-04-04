from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import requests
import os
import json


app = FastAPI()
templates = Jinja2Templates(directory="templates")

server = 'SmartCityReceiver1'
port_number = int(os.environ.get("PORT_NUMBER"))

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search_whole")
async def search_whole():
    url = f"http://localhost:{port_number}/{server}/getData"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Response received successfully:")
            print("Response ", response.text)
            parsed_data = response.json()
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
        print("Parsed ", parsed_data)
        #data = jsonable_encoder(response)
        return parsed_data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
