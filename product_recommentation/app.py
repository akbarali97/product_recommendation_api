
from fastapi import FastAPI, File, UploadFile
from starlette.responses import RedirectResponse

from .utils import predict, read_imagefile
from .utils2 import predict2, get_dominant_colors, get_recommendation


app = FastAPI(
    title='Predicts object in the Image', 
    description='''
                Try this app by uploading any image.
                /api/predict --> To get image prediction.
                /api/get-recommendation  --> To get recommendation based on the image.
                '''
    )

@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")


@app.post("/api/predict")
async def predict_api(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    image = read_imagefile(await file.read())
    prediction = predict(image)
    return prediction

@app.post("/api/get-recommendation")
async def predict_api(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    image = read_imagefile(await file.read())
    colors = get_dominant_colors(image)
    prediction = predict2(image)
    recommendation = get_recommendation(prediction=prediction, colors=colors)
    if len(recommendation) >= 10:
        return recommendation[:10]
    else:
        return recommendation