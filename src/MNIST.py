import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import keras.callbacks
from keras.datasets import mnist
from keras.models import Sequential
from keras import layers
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
from keras.optimizers.schedules import ExponentialDecay

def mnistExample(hidden_layers, neurons, epochs):
    val_acc = []
    weights = []

    class validationAccuracy(keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs=None):
            val_acc.append(logs['val_accuracy'])
            weights.append(model.get_weights())

    validation_accuracy = validationAccuracy()

    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

    # Normalize the data
    train_images, test_images = train_images / 255.0, test_images / 255.0

    train_images, X_val, train_labels, y_val = train_test_split(train_images, train_labels, test_size=0.2, random_state=42)
    train_labels = to_categorical(train_labels)
    y_val = to_categorical(y_val)
    test_labels = to_categorical(test_labels)

    input_layer = layers.Input(shape=(28, 28, 1))
    output_layer = layers.Dense(10, activation='softmax')

    model = Sequential()
    model.add(input_layer)

    for layer in range(hidden_layers):
        model.add(layers.Conv2D(neurons[layer], kernel_size=(3, 3), activation='relu'))
        model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Flatten())
    model.add(layers.Dense(8, activation='relu'))
    model.add(output_layer)

    # Learning rate schedule
    lr_schedule = ExponentialDecay(initial_learning_rate=0.001, decay_steps=10000, decay_rate=0.9)
    model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=lr_schedule), metrics=['accuracy'])

    # Early stopping
    early_stopping = EarlyStopping(monitor='val_loss', patience=3)

    model.fit(
        train_images, train_labels,
        epochs=epochs,
        validation_data=(X_val, y_val),
        callbacks=[validation_accuracy, early_stopping]
    )

    y_pred = model.predict(test_images)
    loss, accuracy = model.evaluate(test_images, test_labels)
    print('Test loss:', loss)
    print('Test accuracy:', accuracy)

    plt.figure()
    plt.plot(range(len(val_acc)), val_acc)
    plt.show()
    return(weights, val_acc, loss, accuracy, y_pred)

def generateNeuronArray(hidden_layer_count, neuron_count):
        return [neuron_count] * hidden_layer_count

mnistExample(3, generateNeuronArray(3,2), 5)