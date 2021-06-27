
def train_model():

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(400, 400, 3)),
        keras.layers.Conv2D(32,kernel_size=3,strides=(1,1),activation='relu', padding='same'),
        keras.layers.Conv2D(32,kernel_size=3,strides=(2,2),activation='relu', padding='same'),
        keras.layers.Conv2D(64,kernel_size=3,strides=(1,1),activation='relu', padding='same'),
        keras.layers.Conv2D(64,kernel_size=3,strides=(2,2),activation='relu', padding='same'),
        keras.layers.Conv2D(128,kernel_size=3,strides=(1,1),activation='relu', padding='same'),
        keras.layers.Conv2D(128,kernel_size=3,strides=(2,2),activation='relu', padding='same'),
        keras.layers.Conv2D(256,kernel_size=3,strides=(1,1),activation='relu', padding='same'),
        keras.layers.Conv2D(256,kernel_size=3,strides=(2,2),activation='relu', padding='same'),
        keras.layers.GlobalAveragePooling2D(),
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(10, activation=tf.nn.softmax)
    ])