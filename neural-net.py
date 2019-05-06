
from keras import Sequential
from keras.layers import Dense
import numpy as np

#HYPERPARAMETERS
NUM_ITERATIONS = 150
NUM_HIDDEN_NODES = 8
BATCH_SIZE = 32 # larger batch size means faster training, in general

NUM_FEATURES = 8 # change this later
trainingData = [] # add features here
trainingLabels = [] # real or fake classification labels
validationData = []
validationLabels = []

#create model
model = Sequential()
model.add(Dense(NUM_HIDDEN_NODES, input_dim=NUM_FEATURES, activation='relu')) #first hidden layer
model.add(Dense(NUM_HIDDEN_NODES, activation='relu')) # second hidden layer
model.add(Dense(1, activation='sigmoid')) # output layer
model.compile(
    loss='binary_crossentropy', 
    optimizer='adam', 
    metrics=['accuracy'],
    validation_data = (validationData, validationLabels)
)

results = model.fit(trainingData, trainingLabels, epochs=NUM_ITERATIONS, batch_size=BATCH_SIZE)
print("Test-Accuracy:", np.mean(results.history["val_acc"]))