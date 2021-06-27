from PIL import Image
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.image import resize

from .db import db

# from tensorflow.keras.applications.resnet50 import ResNet50
# from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

# from tensorflow.keras.applications import DenseNet121
# from tensorflow.keras.applications.densenet import preprocess_input, decode_predictions

# from tensorflow.keras.applications import MobileNet
# from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions

from tensorflow.keras.applications import Xception
from tensorflow.keras.applications.xception import preprocess_input, decode_predictions

def predict2(img: Image.Image):
    '''
    This function takes an input image of PIL format.
    Returns a prediction of list of dictionaries with predicted `class` and predicted `confidence`
    '''

    img_width, img_height, chnl = 299, 299, 3
    input_shape=(img_width, img_height, chnl)
    model = Xception(weights="imagenet", input_shape=input_shape)
    # model = ResNet50(weights='imagenet', input_shape=input_shape)
    # model = DenseNet121(weights='imagenet', input_shape=input_shape)
    # model = MobileNet(weights="imagenet", input_shape=input_shape)
    
    x = image.img_to_array(img.resize((img_width, img_height)))
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # # To display the processed input image
    # image.array_to_img(x[0]).show()

    result = decode_predictions(model.predict(x), top=3)[0]
    response = []
    for i, res in enumerate(result):
        resp = {}
        resp["class"] = res[1]
        resp["confidence"] = round(res[2]*100, 2)
        response.append(resp)
    return response

def get_recommendation(prediction: list, colors: list):
    '''
    This funtion takes in the list of predictions and returns a list of ids of products that are similar
    to the predicted product. If the prediction is less than 80% then return the product's ids in the ratio
    of the prediction.
    '''
    from db import db
    max_confident_item =  max(prediction, key=lambda x:x['confidence'])
    result = db(articletype=max_confident_item['class'], colors=colors)
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
        # dominant_color = webcolors.rgb_to_name()

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

