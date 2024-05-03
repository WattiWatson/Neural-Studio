from sklearn import datasets
import numpy as np
import os
import eel
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import keras.callbacks
from sklearn.metrics import confusion_matrix


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
    val_acc = []
    weight_dict = {}
    model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])
    
    class validationAccuracy(keras.callbacks.Callback):
        # Runs at the end of each epoch
        def on_epoch_end(self, epoch, logs=None):
            val_acc.append(logs['val_accuracy'])
            
            for layer in range(len(self.model.layers)):
                # Weights
                w = model.layers[layer].get_weights()[0]
                
                for neuron in range(len(w)):
                    # Save weights and biases to dictionary
                    if epoch == 0:
                        # Create new array to hold weights and biases
                        weight_dict[f"layer_{str(layer+1)}_neuron_{str(neuron+1)}"] = w[neuron]
                    else:
                        # Append new weights to existing array
                        weight_dict[f"layer_{str(layer+1)}_neuron_{str(neuron+1)}"] = np.dstack((weight_dict[f"layer_{str(layer+1)}_neuron_{str(neuron+1)}"], w[neuron]))

    validation_accuracy = validationAccuracy()
    model.fit(X_train, y_train, epochs=epochs, validation_data=(X_val, y_val), callbacks=[validation_accuracy])
    return val_acc, weight_dict

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    loss, accuracy = model.evaluate(X_test, y_test)
    print('Test loss:', loss)
    print('Test accuracy:', accuracy)
    return y_pred, loss, accuracy

def plot_results(val_acc, epochs):
    plt.figure()
    plt.plot(range(epochs), val_acc)
    plt.title("Accuracy Graph")
    plt.show()
    
def get_last_weights(weights_dict):
    strengthArray = []
    for key in weights_dict:
        if(not(str(key).startswith("bias"))):
            # Get the weights from the last epoch
            last_weights = weights_dict[key][:, :, -1]
            for lw in last_weights:
                for w in lw:
                    strengthArray.append(float(w))
    return strengthArray

@eel.expose
def get_epoch_weights(weights_dict, curr_epoch):
    strengthArray = []
    for key in weights_dict:
        if(not(str(key).startswith("bias"))):
            # Get the weights from the last epoch
            curr_weights = weights_dict[key][:, :, curr_epoch]
            for cw in curr_weights:
                for w in cw:
                    strengthArray.append(float(w))
    return strengthArray

def buildModel(hidden_layers, neurons, epochs):
    X, y = load_data()
    X_train, X_test, X_val, y_train, y_test, y_val = preprocess_data(X, y)
    model = build_model(hidden_layers, neurons)
    val_acc, weights_dict = train_model(model, X_train, y_train, X_val, y_val, epochs)
    y_pred, loss, accuracy = evaluate_model(model, X_test, y_test)
    plot_results(val_acc, epochs)
    return get_last_weights(weights_dict), val_acc, epochs, loss, accuracy, y_pred, weights_dict