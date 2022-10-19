from calendar import c
import os
import pandas as pd
from xml.dom import HIERARCHY_REQUEST_ERR
from config.config import ALLOWED, EXTENSION_FILE
from config.autorization import Credenciales


class UtilReceivedFile:
    def __init__(self, path_guardar_archivo_recibido: str, nombres_parametros: dict):
        self.nombres_parametros = nombres_parametros
        self.nombre_guardar_archivo = path_guardar_archivo_recibido
        print("Ruta Guardado archivo recibido: " + self.nombre_guardar_archivo)

    @staticmethod
    def evaluar_extension_archivo(filename):
        tiene_punto = "." in filename
        if tiene_punto:
            extension_archivo = filename.split(".", 1)[1].lower()
            if extension_archivo in ALLOWED:
                return True
        return False

    def validar_archivo(self, request):
        if self.nombres_parametros[EXTENSION_FILE] not in request.files:
            return False

        nombre_imagen_recibida = request.files[self.nombres_parametros[EXTENSION_FILE]]
        if nombre_imagen_recibida.filename == "":
            return False

        if self.evaluar_extension_archivo(nombre_imagen_recibida.filename):
            self.save_file(nombre_imagen_recibida)
            return True

    def save_file(self, nombre_imagen_recibida):
        nombre_imagen_recibida.save(self.nombre_guardar_archivo)

    def validar_credenciales(self, request):
        form = request.form.to_dict()
        username = form.get("username")
        password = form.get("password")
        print("\t"*2, f"Username ({Credenciales.USER}): " + username)
        print("\t"*2, f"Password ({Credenciales.PASSWORD}): " + password)
        
        if username == Credenciales.USER and password == Credenciales.PASSWORD:
            print("\t"*2, "Credenciales correctas")
            return True
        return False

    def validar_integridad_archivos(self, path_descomprimir, min_filas=2):
        folder_ok = []
        folder_bad = []
        summary = dict(folder="", file=dict(q="",c="",r=""))
        for folder in os.walk(path_descomprimir):
            # print(folder)
            carpeta = folder[0]
            summary["folder"] = carpeta.split(os.sep)[-1]
            summary["file"] = dict()
            archivos = folder[2]
            ok = False
            if len(archivos) >= 3:
                hay_q = "q.csv" in archivos
                hay_c = "c.csv" in archivos
                hay_r = "r.csv" in archivos
                if hay_q and hay_c and hay_r:
                    ok = True
                else:
                    folder_bad.append((summary["folder"], "No estan todos los archivos q,c,r"))
            else:
                if len(summary["folder"]) > 1:
                    folder_bad.append((summary["folder"], "Hay muy pocos archivos, recuerde que deben existir los archivos: q.csv, c.csv, r.csv"))
            
            if ok:
                for file in archivos:
                    path_file = os.path.join(carpeta, file)
                    
                    # validar que el archivo no este vacio
                    name_file = file.split(".")[0].split(os.sep)[-1]
                    if os.stat(path_file).st_size == 0:                    
                        summary["file"][name_file] = 0
                    else:
                        data_file = pd.read_csv(path_file, index_col=False)
                        cantidad_filas = len(data_file.axes[0])
                        summary["file"][name_file] = cantidad_filas
                if summary['folder'] != "noanswer":
                    if summary["file"]["q"] >= min_filas and summary['file']['r'] >= min_filas:
                        folder_ok.append((summary["folder"], "OK"))
                    else:
                        fail_q = False
                        fail_r = False
                        if summary["file"]["q"] < min_filas:
                            fail_q = True

                        if summary["file"]["r"] < min_filas:
                            fail_r = True

                        if fail_q and fail_r:
                            folder_bad.append((summary["folder"], f"q y r tienen menos de {min_filas} filas"))
                        elif fail_q:
                            folder_bad.append((summary["folder"], f"q tiene menos de {min_filas} filas"))
                        elif fail_r:
                            folder_bad.append((summary["folder"], f"r tiene menos de {min_filas} filas"))
                    print("\t"*3, summary)
        
        if len(folder_bad) > 0:
            print("\t"*2, "Archivos con problemas")
            for folder in folder_bad:
                print("\t"*3, folder)
            return False, folder_bad
        else:
            print("\t"*2, "Archivos OK")
            return True, folder_ok