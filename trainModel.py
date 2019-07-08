import numpy as np
import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from keras.layers import Dense,Flatten, Conv2D
from keras.layers import MaxPooling2D, Dropout
from keras.utils import np_utils, print_summary
import tensorflow as tf
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
from keras.callbacks import TensorBoard

def Model(image_x, image_y):
    classes = 15
    model = Sequential()
    model.add(Conv2D(128, (5, 5), input_shape=(image_x, image_y, 1), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2,2), padding='same'))
    model.add(Conv2D(64, (4, 4), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.6))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.6))
    model.add(Dense(classes, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    filepath = "WeightsOfQuickDraw.h5"
    checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    callbacks_list = [checkpoint]
    return model, callbacks_list


def main():
    with open("features", "rb") as f:
        features = np.array(pickle.load(f))
    with open("labels", "rb") as f:
        labels = np.array(pickle.load(f))
    features, labels = shuffle(features, labels)
    labels = np_utils.to_categorical(labels)
    train_x, test_x, train_y, test_y = train_test_split(features, labels, random_state=0,test_size=0.1)
    train_x = train_x.reshape(train_x.shape[0], 28, 28, 1)
    test_x = test_x.reshape(test_x.shape[0], 28, 28, 1)
    print ("train_X: " + str(train_x.shape))
    print("test_X: " + str(test_x.shape))
    model, callbacks_list = Model(28, 28)
    print_summary(model)
    summary = model.fit(train_x, train_y, validation_data=(test_x, test_y), epochs=16, batch_size=64,
                  callbacks=[TensorBoard(log_dir="QuickDraw")])
    #plot result acc
    plt.plot(summary.history['acc'])
    plt.title("Model Accuracy")
    plt.ylabel("Accuracy")
    plt.xlabel("Epochs")
    plt.legend(['train'], loc='upper right')
    plt.show()

    #plot loss result
    plt.plot(summary.history['loss'])
    plt.title("Model Loss")
    plt.ylabel("Loss")
    plt.xlabel("Epochs")
    plt.legend(['train'], loc='upper right')
    plt.show()
    model.save('QuickDraw.h5')


main()
