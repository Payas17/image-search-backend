from fastapi import FastAPI, WebSocket
from fastapi.requests import Request
from starlette.staticfiles import StaticFiles

import config
from app.image_searcher import ImageSearcher
from config import settings

app = FastAPI()
app.mount("/static", StaticFiles(directory="front/javascripts"), name="static")


@app.get("/")
async def get(request: Request):
    return settings.templates.TemplateResponse("browser.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        file = await websocket.receive_bytes()
        image_searcher = ImageSearcher(file)
        label = image_searcher.identify_object()
        # if not label:
        #     response = {"found": False, "url": None}
        # else:
        #     image_searcher.search_products(label, limit=config.settings.products_amount)
        #     url = image_searcher.get_similar_product_url()
        #     response = {"found": True, "url": url}
        await websocket.send_json({"found": False, "url": None})
