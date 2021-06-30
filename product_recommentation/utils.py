from io import BytesIO

import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.applications.imagenet_utils import decode_predictions

def predict(image: Image.Image) -> list:
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


def predict2(image: Image.Image):
    import tensorflow.keras
    from PIL import ImageOps
    import numpy as np
    # To remove the info logging from printing out in the terminal
    np.set_printoptions(suppress=True)

    # load the model
    model = load_trained_model()

    # Process the data
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    # predict the image
    data = model.predict(data)
    [pred] = np.argmax(data, axis=-1)
    labels = load_json_data()
    pred = labels[str(pred)]
    print(pred)
    return [pred]

model = None
def load_trained_model():
    global model
    if model is None:
        from tensorflow.keras.models import load_model
        model = load_model(filepath='./assets/keras_model.h5', compile=False)
    return model

labels = None
def load_json_data() -> dict():
    global labels
    if labels is None:
        import json
        with open('./assets/labels.json') as f:
            labels = json.load(f)
    return labels
    


def get_recommendation(prediction: list, colors: list):
    from .db import db
    result = db(articletype=prediction[0],colors=colors)
    return result

def get_dominant_colors(img: Image.Image, numcolors=10, resize=299):
    # Resize image to speed up processing 
    img.thumbnail((resize, resize))
    # Reduce to palette
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=numcolors)
    # Find dominant colors
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    colors = list()
    for i in range(3):
        palette_index = color_counts[i][1]
        dominant_color = palette[palette_index*3:palette_index*3+3]
        dominant_color = get_colour_name(tuple(dominant_color))
        colors.append(str(dominant_color))
    return colors

def get_colour_name(requested_colour: tuple):
    import webcolors
    try:
        color_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        min_colours = {}
        for key, name in webcolors.css3_hex_to_names.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        return min_colours[min(min_colours.keys())]
    return color_name