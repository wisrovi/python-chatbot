import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle

import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

nltk.download('popular', quiet=True)  # for downloading popular packages
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


def create_model(size_input, size_output):
    # creazione del modello
    model = Sequential()
    model.add(Dense(128, input_shape=(size_input,), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(size_output, activation='softmax'))

    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    return model


def train_model():
    lemmatizer = WordNetLemmatizer()
    words = []
    classes = []
    documents = []
    ignore_words = ['?', '!']

    print("Loading data...")
    with open('model/data_train/intents.json') as file:
        intents = json.load(file)
    print(intents)

    # intents: gruppi di conversazioni-tipo
    # patterns: possibili interazioni dell'utente
    print("Processing data...")
    for intent in intents['intents']:
        for pattern in intent['patterns']:

            # tokenizzo ogni parola
            w = nltk.word_tokenize(pattern)
            words.extend(w)
            # aggiungo all'array documents
            documents.append((w, intent['tag']))

            # adding classes to our class list
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]

    print("Saving data...")
    pickle.dump(words, open('model/words.pkl', 'wb'))
    pickle.dump(classes, open('model/classes.pkl', 'wb'))

    # preparazione per l'addestramento della rete
    print("Preparing data...")
    training = []
    output_empty = [0] * len(classes)
    for doc in documents:
        # bag of words
        bag = []
        # lista di tokens
        pattern_words = doc[0]
        # lemmatizzazione dei token
        pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
        # se la parola matcha, inserisco 1, altriment 0
        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)

        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1

        training.append([bag, output_row])

    print("Training data...")
    training = np.array(training)
    # creazione dei set di train e di test: X - patterns, Y - intents
    train_x = list(training[:, 0])
    train_y = list(training[:, 1])

    model = create_model(len(train_x[0]), len(train_y[0]))

    print("Training model...")
    # fitting and saving the model
    hist = model.fit(np.array(train_x), np.array(train_y), epochs=300, batch_size=5, verbose=1)
    model.save('model/chatbot_model.h5', hist)

    print("Model trained and saved!")

    # print("history: ", hist.history)
    # print("keys history: ", hist.history.keys())

    # hallar promedio del array de loss
    loss = hist.history['loss']
    loss_avg = sum(loss) / len(loss)
    loss_avg = round(loss_avg*100, 2)
    print("loss_avg: ", loss_avg)

    # hallar promedio del array de accuracy
    accuracy = hist.history['accuracy']
    accuracy_avg = sum(accuracy) / len(accuracy)
    accuracy_avg = round(accuracy_avg*100, 2)
    print("accuracy_avg: ", accuracy_avg)
    
    return f"{loss_avg}%", f"{accuracy_avg}%"
