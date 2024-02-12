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
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


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
    weights_dict = {}
    model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.001), metrics=['accuracy'])
    
    class validationAccuracy(keras.callbacks.Callback):
        def __init__(self):
            self.val_acc = val_acc
            self.weight_dict = weights_dict
            
        # Runs at the end of each epoch
        def on_epoch_end(self, epoch, logs=None):
            self.val_acc.append(logs['val_accuracy'])
            # weights.append(model.get_weights())
            
            for layer in range(len(self.model.layers)):
                # Weights
                w = self.model.layers[layer].get_weights()[0]
                # Bias
                b = self.model.layers[layer].get_weights()[1]
                print(f"Layer {layer} has weights of shape {np.shape(w)} and biases of shape {np.shape(b)}")
                
                # Save weights and biases to dictionary
                if epoch == 0:
                    # Create new array to hold weights and biases
                    self.weight_dict[f"weight_{str(layer+1)}"] = w
                    self.weight_dict[f"bias_{str(layer+1)}"] = b
                else:
                    # Append new weights to new 
                    self.weight_dict[f"weight_{str(layer+1)}"] = np.dstack((self.weight_dict[f"weight_{str(layer+1)}"], w))
                    self.weight_dict[f"bias_{str(layer+1)}"] = np.dstack((self.weight_dict[f"bias_{str(layer+1)}"], b))

    validation_accuracy = validationAccuracy()
    model.fit(X_train, y_train, epochs=epochs, validation_data=(X_val, y_val), callbacks=[validation_accuracy])
    return val_acc, weights_dict

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    loss, accuracy = model.evaluate(X_test, y_test)
    print('Test loss:', loss)
    print('Test accuracy:', accuracy)
    return y_pred, loss, accuracy

def plot_results(val_acc, epochs):
    plt.figure()
    plt.plot(range(epochs), val_acc)
    plt.show()
    
def normalize_weights(weights):
    # Flatten all weights and concatenate into a single array
    flattened_weights = np.concatenate([w.flatten() for layer_weights in weights for w in layer_weights])
    # Normalize weights to range [0, 1]
    normalized_weights = (flattened_weights - np.min(flattened_weights)) / (np.max(flattened_weights) - np.min(flattened_weights))
    print(weights)
    return normalized_weights

def buildModel(hidden_layers, neurons, epochs):
    X, y = load_data()
    X_train, X_test, X_val, y_train, y_test, y_val = preprocess_data(X, y)
    model = build_model(hidden_layers, neurons)
    val_acc, weights = train_model(model, X_train, y_train, X_val, y_val, epochs)
    y_pred, loss, accuracy = evaluate_model(model, X_test, y_test)
    # plot_results(val_acc, epochs)
    return weights, val_acc, loss, accuracy, y_pred