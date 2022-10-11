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
        df = pd.DataFrame(patterns, columns=['patterns'])

        """
        guardar dataframe en q.csv en la carpeta del tag
        """
        df.to_csv("nuevos_chats/" + tag['tag'] + "/q.csv", index=False, header=False)
        




def cargar_nuevos_chats():
    """
    Carga los nuevos chats que se encuentran en la carpeta 'nuevos_chats'
    """
    chats = []
    for archivo in os.listdir(FOLDER):
        with open(os.path.join(FOLDER, archivo), "r", encoding="utf-8") as f:
            chats.append(json.load(f))
    return chats


if __name__ == "__main__":
    convertir_intents_a_carpetas()