FOLDER = "nuevos_chats"

import os
import pandas as pd
import json
from turtle import clear


def convertir_intents_a_carpetas():
    """
    Convierte los intents a carpetas para que puedan ser leídos por el modelo
    """
    FOLDER_DATA_TRAIN = "data_train/"
    name_file = FOLDER_DATA_TRAIN + "intents.json"    

    """
    Carga los intents json
    """
    with open(name_file, "r", encoding="utf-8") as f:
        intents = json.load(f)
    
    for tag in intents['intents']:
        """
        Crea una carpeta con el nombre del tag
        """
        print("Creando carpeta: " + tag['tag'])
        os.makedirs("nuevos_chats/" + tag['tag'], exist_ok=True)


        patterns = tag['patterns']
        """
        Convertir lista de patterns a dataframe
        """
        df = pd.DataFrame(patterns, columns=['patterns'], index=None, dtype=None, copy=False)

        """
        guardar dataframe en q.csv en la carpeta del tag
        """
        df.to_csv("nuevos_chats/" + tag['tag'] + "/q.csv", index=False, header=False)

        responses = tag['responses']
        """
        Convertir lista de responses a dataframe
        """
        df = pd.DataFrame(responses, columns=['responses'])

        """
        Guardar dataframe en r.csv en la carpeta del tag
        """
        df.to_csv("nuevos_chats/" + tag['tag'] + "/r.csv", index=False, header=False)


        responses = tag['context']
        """
        Convertir lista de responses a dataframe
        """
        df = pd.DataFrame(responses, columns=['context'])

        """
        Guardar dataframe en c.csv en la carpeta del tag
        """
        df.to_csv("nuevos_chats/" + tag['tag'] + "/c.csv", index=False, header=False)
        

def cargar_nuevos_chats():
    """
    Carga los nuevos chats que se encuentran en la carpeta 'nuevos_chats' en un archivo intents.json
    """
    FOLDER_DATA_TRAIN = "data_train/"
    name_file = FOLDER_DATA_TRAIN + "intents.json"    

    intents = {}

    """
    Carga los chats de la carpeta 'nuevos_chats'
    """
    lista_intents = []
    for tag in os.listdir(FOLDER):
        """
        Carga los patterns
        """
        print("Cargando patterns de: " + tag)
        try:
            df = pd.read_csv(FOLDER + "/" + tag + "/q.csv", header=None, encoding="utf-8")
            patterns = df[0].tolist()
        except:
            patterns = []

        """
        Cargo los responses
        """
        print("Cargando responses de: " + tag)
        try:
            df = pd.read_csv(FOLDER + "/" + tag + "/r.csv", header=None, encoding='utf-8')
            responses = df[0].tolist()
        except:
            responses = []

        """
        Cargo los context
        """
        print("Cargando context de: " + tag)
        try:
            df = pd.read_csv(FOLDER + "/" + tag + "/c.csv", header=None, encoding='utf-8')
            context = df[0].tolist()
        except:
            context = []

        print("Context: ", context)
        """
        Convertir nan a string vacío
        """
        context = [str(x) for x in context]
        context = [x for x in context if x != 'nan']
                   

        """
        Agrega los patterns y responses al intents json
        """
        lista_intents.append({
            "tag": tag,
            "patterns": patterns,
            "responses": responses,
            "context": context
        })

    """
    Guarda el intents json
    """
    print("Guardando intents.json")
    # print(lista_intents)
    lista_intents = {
        "intents": lista_intents
    }
    with open(name_file, "w", encoding="utf-8") as f:
        json.dump(lista_intents, f, ensure_ascii= False, indent= 4)
    

if __name__ == "__main__":
    convertir_intents_a_carpetas()
    cargar_nuevos_chats()