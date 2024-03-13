from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from data_handler import search_whole_table

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search_whole/{table}")
async def search_whole(table: str):
    result, query_time = search_whole_table(table)
    response_data = {
        'query_time': query_time,  # Add the query time to the response data
        'result': result
    }
    return JSONResponse(content=response_data)