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

def irisExample(hidden_layers, neurons, epochs):
    val_acc = []
    weights = []


    class validationAccuracy(keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs=None):
            val_acc.append(logs['val_accuracy'])
            weights.append(model.get_weights())


    # Create callback instance

    validation_accuracy = validationAccuracy()



    iris = datasets.load_iris()
    X = iris.data
    y = iris.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.1111, random_state=42)
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)
    y_val = to_categorical(y_val)


    model = Sequential()
    model.add(Dense(4, input_shape=(4,), activation='relu'))  # input layer, will always have the same shape
    for layer in range(hidden_layers):
        model.add(Dense(neurons[layer], activation='relu'))
    model.add(Dense(3, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.001), metrics=['accuracy'])

    # Train the model
    model.fit(
        X_train, y_train,
        epochs=epochs,
        validation_data=(X_val, y_val),
        callbacks=[validation_accuracy]
            )

    # Evaluate the model on the test set
    y_pred = model.predict(X_test)
    loss, accuracy = model.evaluate(X_test, y_test)
    print('Test loss:', loss)
    print('Test accuracy:', accuracy)

    plt.figure()
    plt.plot(range(epochs), val_acc)
    plt.show()
    return(weights, val_acc, loss, accuracy, y_pred)
irisExample(3, [10,12,10], 100)

