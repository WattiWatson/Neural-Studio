'''
    Link between HTML/JavaScript frontend and Python
'''
import eel
import sys, platform
import main
eel.init("./src/gui")

NS = main.Neural_Studio()

# Expose function to start model from JavaScript
@eel.expose
def triggerBuildIrisModel(hidden_layers, neurons, training_epochs):
    weights, val_acc, loss, accuracy, y_pred = NS.buildIrisModel(hidden_layers, neurons, training_epochs)
    return weights

@eel.expose
def triggerBuildMNISTModel(hidden_layers, neurons, training_epochs):
    weights, val_acc, loss, accuracy, y_pred = NS.buildMNISTModel(hidden_layers, neurons, training_epochs)
    return weights

def loadFrontend(width, height):
    try:
        # Try to start application using Chrome
        eel.start("iris_viz.html", size=(width, height))
    except EnvironmentError:
        # If Chrome is not installed, fallback to default browser
        eel.start("iris_viz.html", size=(width, height), mode='default')
