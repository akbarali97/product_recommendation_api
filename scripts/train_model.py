#setting up all the essentials
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg


#machine learning libraries 
from keras.models import Sequential, Model
from keras_preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Activation, Flatten, Dropout, BatchNormalization, Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras import regularizers, optimizers
from keras.applications.mobilenet_v2 import MobileNetV2
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler

import os # accessing directory structure


#import and setup training dataset
TRAINING_DATASET_PATH = "../dataset/"
training_data = pd.read_csv(TRAINING_DATASET_PATH + "styles.csv", error_bad_lines=False)
training_data['image'] = training_data.apply(lambda row: str(row['id']) + ".jpg", axis=1)
training_data = training_data.sample(frac=1).reset_index(drop=True)
training_data.head(10)