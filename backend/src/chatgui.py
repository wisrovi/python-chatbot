import nltk, json, random, pickle
from nltk.stem import WordNetLemmatizer

nltk.download('popular', quiet=True) # for downloading popular packages
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from tensorflow.keras.models import load_model

classes = words = intents = model = None
def leer_data():
    global classes, words, intents, model

    model = load_model('/model/chatbot_model.h5')
    intents = json.loads(open('/data_train/intents.json').read())
    words = pickle.load(open('/model/words.pkl','rb'))
    classes = pickle.load(open('/model/classes.pkl','rb'))

# preprocessamento input utente
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# creazione bag of words
def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def calcola_pred(sentence, model):
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getRisposta(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def inizia(msg, charge=False):
    if charge:
        leer_data()
    ints = calcola_pred(msg, model)
    res = getRisposta(ints, intents)
    return res

utente = 'hello'
res = inizia(utente, charge=True)

if __name__ == "__main__":
    print('Benvenuto! Per uscire, scrivi "Esci"')
    while utente != 'esci':
        utente = str(input(""))
        res = inizia(utente)
        print('AI:' + res)