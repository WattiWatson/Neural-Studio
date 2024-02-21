import keras.callbacks
from tensorflow.keras.datasets import mnist
from keras.models import Sequential
from keras import layers
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras.utils import to_categorical


def mnistExample(hidden_layers, neurons, epochs):
    val_acc = []
    weights = []

   #callback class to save validation accuracy and weights after each epoch
    class validationAccuracy(keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs=None):
            val_acc.append(logs['val_accuracy'])
            weights.append(model.get_weights())


    # Create callback instance
    validation_accuracy = validationAccuracy()

    #import data from mnist
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

    #split training images into validation set
    train_images, X_val, train_labels, y_val = train_test_split(train_images, train_labels, test_size=0.2, random_state=42)
    train_labels = to_categorical(train_labels)
    y_val = to_categorical(y_val)
    test_labels = to_categorical(test_labels)
    # Input layer
    input_layer = (layers.Input(shape=(28, 28, 1)))  # 28x28 grayscale image
    # Output layer
    output_layer = (layers.Dense(10, activation='softmax'))  # classified as a number 0-9

    #layers are added to the model sequentially
    model = Sequential()
    model.add(input_layer)

    #a convolutional layer and maxpooling layer is added based on the number of hidden layers passed to the function
    for layer in range(hidden_layers):
        model.add(layers.Conv2D(neurons[layer], kernel_size=(3, 3), activation='relu'))
        model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    #Convolutional output is flattened and passed through a fully connected layer
    model.add(layers.Flatten())
    model.add(layers.Dense(8, activation='relu'))
    model.add(output_layer)
    model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.001), metrics=['accuracy'])

    # Train the model
    model.fit(
        train_images, train_labels,
        epochs=epochs,
        validation_data=(X_val, y_val),
        callbacks=[validation_accuracy]
    )

    # Evaluate the model on the test set
    y_pred = model.predict(test_images)
    loss, accuracy = model.evaluate(test_images, test_labels)
    print('Test loss:', loss)
    print('Test accuracy:', accuracy)

    plt.figure()
    plt.plot(range(epochs), val_acc)
    plt.show()
    return(weights, val_acc, loss, accuracy, y_pred)
