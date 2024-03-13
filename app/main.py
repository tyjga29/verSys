from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from data_handler import execute_query

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/start_query")
async def start_query(query: str = Query(...)):
    result, query_time = execute_query(query)
    response_data = {
        'query_time': query_time,  # Add the query time to the response data
        'result': result
    }
    return JSONResponse(content=response_data)

