from sklearn import datasets
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import keras.callbacks
from sklearn.metrics import confusion_matrix

class validationAccuracy(keras.callbacks.Callback):
    def __init__(self, model):
        self.val_acc = []
        self.weights = []
        self.model = model

    def on_epoch_end(self, epoch, logs=None):
        self.val_acc.append(logs['val_accuracy'])
        self.weights.append(self.model.get_weights())

def load_data():
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    return X, y

def preprocess_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.1111, random_state=42)
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)
    y_val = to_categorical(y_val)
    return X_train, X_test, X_val, y_train, y_test, y_val

def build_model(hidden_layers, neurons):
    model = Sequential()
    model.add(Dense(4, input_shape=(4,), activation='relu'))  # input layer
    for layer in range(hidden_layers):
        model.add(Dense(neurons[layer], activation='relu'))  # hidden layers
    model.add(Dense(3, activation='softmax'))  # output layer
    return model

def train_model(model, X_train, y_train, X_val, y_val, epochs):
    model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.001), metrics=['accuracy'])
    validation_accuracy = validationAccuracy(model)
    model.fit(X_train, y_train, epochs=epochs, validation_data=(X_val, y_val), callbacks=[validation_accuracy])
    return validation_accuracy

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    loss, accuracy = model.evaluate(X_test, y_test)
    print('Test loss:', loss)
    print('Test accuracy:', accuracy)
    return y_pred, loss, accuracy

def plot_results(validation_accuracy, epochs):
    plt.figure()
    plt.plot(range(epochs), validation_accuracy.val_acc)
    plt.show()

def buildModel(hidden_layers, neurons, epochs):
    X, y = load_data()
    X_train, X_test, X_val, y_train, y_test, y_val = preprocess_data(X, y)
    model = build_model(hidden_layers, neurons)
    validation_accuracy = train_model(model, X_train, y_train, X_val, y_val, epochs)
    y_pred, loss, accuracy = evaluate_model(model, X_test, y_test)
    plot_results(validation_accuracy, epochs)
    return validation_accuracy.weights, validation_accuracy.val_acc, loss, accuracy, y_pred