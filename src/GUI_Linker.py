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
    tArr = []
    weights, val_acc, epochs, loss, accuracy, y_pred, weights_dict = NS.buildIrisModel(hidden_layers, neurons, training_epochs)
    tArr.append(weights)
    tArr.append(val_acc)
    tArr.append(accuracy)
    tArr.append(loss)
    tArr.append(epochs)
    tArr.append(weights_dict)
    return tArr
@eel.expose
def triggerGetIrisValidationAccuracy():
    return NS.getIrisValidationAccuracy
@eel.expose
def triggerGetIrisEpochs():
    return NS.getIrisEpochs

# @eel.expose
# def triggerBuildMNISTModel(hidden_layers, neurons, training_epochs):
#     weights, val_acc, epochs, loss, accuracy, y_pred = NS.buildMNISTModel(hidden_layers, neurons, training_epochs)
#     return weights

def loadFrontend(width, height):
    try:
        # Try to start application using Chrome
        eel.start("index.html", size=(width, height))
    except EnvironmentError:
        # If Chrome is not installed, fallback to default browser
        eel.start("index.html", size=(width, height), mode='default')
