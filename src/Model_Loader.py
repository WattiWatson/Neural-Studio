'''
    Loads the different models and has functions to interpret the data
'''

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.models import load_model as tensor_load_model
from tensorflow.keras.layers import Dense, Input
from sklearn import datasets
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import random

class Iris_Model:
    def __init__(self, model_path):
        self.model_path = model_path
        
    def get_model(self):
        # Load data
        data = datasets.load_iris()
        
        # Get values
        self.x = data.data
        self.y = data.target
        self.z = data.target_names

        # Split the dataset
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=0.3)
        
        # Return the loaded iris model
        self.loaded_iris_model = tensor_load_model(self.model_path)
        return self.loaded_iris_model
        
    # def get_weights(self):
    #     # Check to ensure necessary variables are set
    #     if(self.loaded_iris_model is not None):
    #         # Get weights array
    #         weights = self.loaded_iris_model.get_weights()
    #         return weights
    #     else:
    #         print("Please run 'get_model()' before running 'get_weights()'")
    
    def get_weights(self):
        # Check to ensure necessary variables are set
        if self.loaded_iris_model is not None:
            # Iterate through layers and print weights
            for layer in self.loaded_iris_model.layers:
                if hasattr(layer, 'get_weights'):
                    layer_weights = layer.get_weights()
                    if layer_weights:
                        print(f"Layer: {layer.name}")
                        for i, weights in enumerate(layer_weights):
                            print(f"  Weights {i + 1}: {weights.shape}")
                    else:
                        print(f"Layer: {layer.name} has no weights.")
                else:
                    print(f"Layer: {layer.name} does not have weights (e.g., Flatten layer).")
        else:
            print("Please run 'get_model()' before running 'get_weights()'")
    
    def get_prediction(self, observation_count):
        # Check to ensure necessary variables are set
        if(self.x_test is not None or self.loaded_iris_model is not None):
            prediction = self.loaded_iris_model.predict(self.x_test[:observation_count])
            return prediction
        else:
            print("Please run 'get_model()' before running 'get_prediction()'")
    
    def compare_prediction(self, prediction, observation_count):
        # Check to ensure necessary variables are set
        if(self.y is not None):
            p = np.argmax(prediction, axis=1)
            actual = self.y_test[:observation_count]
            results = {
                "Prediction": p,
                "Actual": actual
            }
            return results
        else:
            print("Please run 'get_model()' before running 'compare_prediction()'")
            
    def get_input_neurons_count(self):
        # Check to ensure necessary variables are set
        if self.loaded_iris_model is not None:
            input_layer = self.loaded_iris_model.layers[0]  # Assuming the input layer is the first layer
            input_shape = input_layer.input_shape
            return input_shape[1] if len(input_shape) > 1 else input_shape[0]
        else:
            print("Please run 'get_model()' before running 'get_input_neurons_count()'")

    def get_output_neurons_count(self):
        # Check to ensure necessary variables are set
        if self.loaded_iris_model is not None:
            output_layer = self.loaded_iris_model.layers[-1]  # Assuming the output layer is the last layer
            output_shape = output_layer.output_shape
            return output_shape[1] if len(output_shape) > 1 else output_shape[0]
        else:
            print("Please run 'get_model()' before running 'get_output_neurons_count()'")

# class MNIST_Model: