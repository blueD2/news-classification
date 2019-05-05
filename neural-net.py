
from keras.models import Sequential
from keras.layers import Dense

#HYPERPARAMETERS
NUM_ITERATIONS = 150
BATCH_SIZE = 32 # larger batch size means faster training, in general

NUM_FEATURES = 8 # change this later
trainingData = [] # add features here
trainingLabels = [] # real or fake classification labels
validationData = []
validationLabels = []

#create model
model = Sequential()
model.add(Dense(12, input_dim=NUM_FEATURES, activation='relu')) #first layer
model.add(Dense(8, activation='relu')) # hidden layer
model.add(Dense(1, activation='sigmoid')) # output layer
model.compile(
    loss='binary_crossentropy', 
    optimizer='adam', 
    metrics=['accuracy'],
    validation_data = (validationData, validationLabels)
)

results = model.fit(trainingData, trainingLabels, epochs=NUM_ITERATIONS, batch_size=BATCH_SIZE)

scores = model.evaluate(validationData, validationLabels)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))