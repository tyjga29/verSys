from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import time
from threading import Timer
from datetime import datetime

from data_handler import search_whole_table

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Caching variables
cache = {}
cache_expiry = 60  # 60 seconds = 1 minute

# Function to fetch data
def fetch_data(table):
    if table in cache and time.time() - cache[table]['timestamp'] < cache_expiry:
        return cache[table]['data']
    else:
        # Make HTTP request to fetch data
        result, query_time = search_whole_table(table)
        timestamp = time.time()
        # Update cache with fetched data and timestamp
        cache[table] = {'data': {'mongo_query': query_time, 'result': result, 'timestamp': timestamp}, 'timestamp': timestamp}
        return {'mongo_query': query_time, 'result': result, 'timestamp': timestamp}

# Function to refresh cache
def refresh_cache():
    cache.clear()
    Timer(cache_expiry, refresh_cache).start()

# Start cache refresh scheduler
refresh_cache()

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search_whole/{table}")
async def search_whole(table: str):
    overall_query_start = time.time()
    data = fetch_data(table)
    overall_query_time = time.time() - overall_query_start
    data['overall_query'] = overall_query_time
    data['timestamp'] = datetime.fromtimestamp(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
    return JSONResponse(content=jsonable_encoder(data))
