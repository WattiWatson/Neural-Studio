import GUI_Linker as GUI
import numpy as np

class Neural_Studio:
    def generateNeuronArray(self, hidden_layer_count, neuron_count):
        return [neuron_count] * hidden_layer_count
    
    def buildIrisModel(self, hidden_layer_count, neuron_count, training_epochs_count):
        import Iris
        neuron_array = self.generateNeuronArray(hidden_layer_count, neuron_count)
        weights, val_acc, loss, accuracy, y_pred = Iris.buildModel(hidden_layer_count, neuron_array, training_epochs_count) # hidden_layers, neurons, training_epcohs
        return weights, val_acc, loss, accuracy, y_pred
    
    def startApplication(self):
        GUI.loadFrontend()

if __name__ == "__main__":
    NS = Neural_Studio()
    
    NS.startApplication()
    
    n = 2
    hl = 2
    # Print weights dictionary
    # weights, iris_val_acc, iris_loss, iris_accuracy, iris_y_pred = NS.buildIrisModel(hl,n,100)
    # for key in weights:
    #     if(not(str(key).startswith("bias"))):
    #         weight_shape = np.shape(weights[key])
    #         last_weights = weights[key][:, :, -1]
    #         # avg_weight = np.mean(last_weights)
    #         # Exclude the epoch count in output
    #         print(f"{str(key)} | shape: {str(weight_shape[0])}, {str(weight_shape[1])} | last weights: {last_weights}")
            
    # num_of_edges = (4 * n) + ((hl - 1) * (n * n)) + (3 * n)
    # print(f"\nNumber of Edges {num_of_edges}\n")
