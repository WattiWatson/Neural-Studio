'''
    Link between HTML/JavaScript frontend and Python
'''
import eel
import sys, platform
import main
eel.init("./src/gui")

NS = main.Neural_Studio()

@eel.expose
def triggerBuildIrisModel(hidden_layers, neurons):
    weights, val_acc, loss, accuracy, y_pred = NS.buildIrisModel(hidden_layers, neurons, 100) # training_epochs
    return weights

def loadFrontend(width, height):
    try:
        eel.start("index.html", size=(width, height))
    except EnvironmentError:
        # If Chrome isn't found, fallback to Microsoft Edge
        if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
            eel.start("index.html", size=(width, height), mode='edge')
        else:
            raise
