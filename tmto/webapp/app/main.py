from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from app.predict import process_image, process_video, process_live_feed
from pathlib import Path

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("templates/index.html") as f:
        return f.read()

@app.post("/predict_image/")
async def predict_image(file: UploadFile = File(...)):
    image = await file.read()
    processed_image = process_image(image)
    return StreamingResponse(processed_image, media_type="image/jpeg")

@app.post("/predict_video/")
async def predict_video(file: UploadFile = File(...)):
    video_path = Path(f"static/uploads/videos/{file.filename}")
    with open(video_path, "wb") as f:
        f.write(await file.read())
    processed_video = process_video(video_path)
    return StreamingResponse(processed_video, media_type="video/mp4")

@app.websocket("/live_feed/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async for frame in websocket.iter_bytes():
        processed_frame = process_live_feed(frame)
        await websocket.send_bytes(processed_frame)

