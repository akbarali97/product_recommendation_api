
from fastapi import FastAPI, File, UploadFile
from starlette.responses import RedirectResponse
from fastapi.responses import FileResponse

from .utils import predict, read_imagefile, predict2, get_dominant_colors, get_recommendation
from settings import IMAGE_PATH

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
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg")
    if not extension:
        return "Image must be jpg or png format!"
    image = read_imagefile(await file.read())
    prediction = predict(image)
    return prediction

@app.post("/api/get-recommendation")
async def predict_api(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg")
    if not extension:
        return "Image must be jpg format!"
    image = read_imagefile(await file.read())
    colors = get_dominant_colors(image)
    prediction = predict2(image)
    recommendation = get_recommendation(prediction=prediction, colors=colors)
    recommendation = recommendation[:10] if len(recommendation) >= 10 else recommendation
    response = {
        'prediction': prediction,
        'recommendation': recommendation,
        'dominent_colors': colors,
        }
    return response


@app.get("/images/{image_id}")
async def get_image(image_id: str):
    image = IMAGE_PATH + image_id + '.jpg'
    return FileResponse(image)