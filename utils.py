from io import BytesIO

import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.applications.imagenet_utils import decode_predictions

def predict(image: Image.Image):
    # loads model
    model = tf.keras.applications.MobileNetV2(weights="imagenet")

    image = np.asarray(image.resize((224, 224)))[..., :3]
    image = np.expand_dims(image, 0)
    image = image / 127.5 - 1.0

    result = decode_predictions(model.predict(image), top=3)[0]

    response = []
    for i, res in enumerate(result):
        resp = {}
        resp["class"] = res[1]
        resp["confidence"] = f"{res[2]*100:0.2f} %"

        response.append(resp)

    return response

def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image