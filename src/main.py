'''
    Main file where the GUI is loaded and parameters are passed to the models
'''

# Import modules
import Model_Creator
import Model_Loader
import GUI

# Create iris model
def create_iris_model(iris_model_path, neuron_count, hidden_layer_count, training_iterations, observation_count):
    iris_model = Model_Creator.Iris_Model()
    iris_model.build_model(neuron_count, hidden_layer_count)
    iris_model.train_model(training_iterations)
    iris_model.save_model(iris_model_path)
    
    iris_model.evaluate_model()
    iris_model_prediction = iris_model.get_prediction(observation_count)
    iris_model.compare_prediction(iris_model_prediction, observation_count)

# Load saved iris model
def load_iris_model(iris_model_path, observation_count):
    iris_model_loader = Model_Loader.Iris_Model(iris_model_path)
    iris_model = iris_model_loader.get_model()
    return iris_model_loader
    # small_predictions = iris_model_loader.get_prediction(observation_count)
    # compare_prediction = iris_model_loader.compare_prediction(small_predictions, observation_count)
    # input_neuron_count = iris_model_loader.get_input_neurons_count()
    # output_neurons_count = iris_model_loader.get_output_neurons_count()

# Variables
iris_model_path = "src/saved_models/iris_model.keras"
neuron_count = 5
hidden_layer_count = 2
training_iterations = 21
small_observation_count = 20

# Create iris model
# create_iris_model(iris_model_path, neuron_count, hidden_layer_count, training_iterations, small_observation_count)

# Load iris model
iml = load_iris_model(iris_model_path, small_observation_count)
input_neuron_count = iml.get_input_neurons_count()
output_neuron_count = iml.get_output_neurons_count()

print(f"Input neuron count: {input_neuron_count}")
print(f"Hidden layer neuron count: {neuron_count}x{hidden_layer_count}")
print(f"Hidden layer weights: {iml.get_weights()}")
print(f"Output neuron count: {output_neuron_count}")

# Launch Test GUI
# app = GUI.QApplication([])
# window = GUI.MainWindow()
# window.show()
# app.exec()
