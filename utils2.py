from PIL import Image
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.image import resize
# from tensorflow.keras.applications.resnet50 import ResNet50
# from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.applications.densenet import preprocess_input, decode_predictions

# from tensorflow.keras.applications import Xception
# from tensorflow.keras.applications.xception import preprocess_input, decode_predictions

from tensorflow.keras.applications import MobileNet
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions

def predict2(img: Image.Image):
    img_width, img_height, chnl = 224, 224, 3
    input_shape=(img_width, img_height, chnl)
    # model = ResNet50(weights='imagenet', input_shape=input_shape)
    # model = DenseNet121(weights='imagenet', input_shape=input_shape)
    # model = Xception(weights="imagenet", input_shape=input_shape)
    model = MobileNet(weights="imagenet", input_shape=input_shape)
    
    x = image.img_to_array(img.resize((img_width, img_height)))
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    result = decode_predictions(model.predict(x), top=3)[0]
    response = []
    for i, res in enumerate(result):
        resp = {}
        resp["class"] = res[1]
        resp["confidence"] = f"{res[2]*100:0.2f} %"
        response.append(resp)
    return response