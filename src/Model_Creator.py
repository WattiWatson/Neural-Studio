'''
    Creates each model and trains them
'''

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn import datasets
from sklearn.model_selection import train_test_split

class Iris_Model:
    def __init__(self):
        # Load the data
        Iris_Model.load_data(self)
    
    def build_model(self, neuron_count, hidden_layer_count):
        # Create sequential model
        self.iris_model = Sequential()
        
        # Create hidden layer
        for i in range(hidden_layer_count):
            self.iris_model.add(Dense(neuron_count, input_shape=(4,), activation="relu"))
        
        # Create output layer
        self.iris_model.add(Dense(3, activation="softmax"))
        
        # Compile the model
        self.iris_model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    
    def load_data(self):
        # Load data
        self.data = datasets.load_iris()
        
        # Get data values
        self.x = self.data.data
        self.y = self.data.target
        self.z = self.data.target_names
        self.feature_names = self.data.feature_names
        
        # Split the dataset
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=0.3)
        
    def train_model(self, training_iterations):
        if(self.iris_model is not None):
            # Fit the model
            self.iris_model.fit(self.x_train, self.y_train, epochs=training_iterations)
        else:
            print("Please run 'build_model()' before running 'train_model()'.")
    
    def save_model(self, saved_model_path):
        if(self.iris_model is not None):
            # Save trained model
            self.iris_model.save(saved_model_path)
        else:
            print("Please run 'build_model()' and 'train_model()' before running 'save_model()'.")
            
    def evaluate_model(self):
        if(self.iris_model is not None and self.x_test is not None):
            # Evaluate loss and accuracy (output: [loss, accuracy])
            self.iris_model.evaluate(self.x_test, self.y_test)
        else:
            print("Please run 'build_model()' and 'train_model()' before running 'evaluate_model()'.")
            
    def get_prediction(self, observation_count):
        if(self.x_test is not None or self.iris_model is not None):
            # Get prediction
            prediction = self.iris_model.predict(self.x_test[:observation_count])
            return prediction
        else:
            print("Please run 'build_model()' before running 'get_prediction()'")

    def compare_prediction(self, prediction, observation_count):
        if(self.y is not None):
            # Get prediction array
            p = np.argmax(prediction, axis=1)
            # Get actual/correct array
            actual = self.y_test[:observation_count]
            # Format the prediction and actual arrays into a dictionary
            results = {
                "Prediction": p,
                "Actual": actual
            }
            return results
        else:
            print("Please run 'build_model()' before running 'compare_prediction()'")
            
# class MNIST_Model:
