import os
from flask import Flask, render_template, jsonify, request, redirect

from src.libraries.UtilReceivedFile import UtilReceivedFile
from src.libraries.UtilZipFile import UtilZipFile
from src.libraries.cargar_nuevos_chats import cargar_nuevos_chats
from src.libraries.train_bot import train_model
import time

app = Flask(__name__)


if os.environ.get("SO") is None:
    filepath = os.path.dirname(os.path.abspath(__file__)) + os.sep + "received_files" + os.sep + "recibido.zip"
    print("Execution in: Local")
else:
    filepath = os.sep + "received_files" + os.sep + "recibido.zip"
    print("Execution in: Docker")


if os.environ.get("SO") is None:
    path_descomprimir = os.path.dirname(os.path.abspath(__file__)) + os.sep + "nuevos_chats" + os.sep
    print("Execution in: Local")
else:
    path_descomprimir = os.sep + "nuevos_chats" + os.sep
    print("Execution in: Docker")


util = UtilReceivedFile(path_guardar_archivo_recibido=filepath, nombres_parametros={"zip": "file1"})
zip = UtilZipFile(filepath, ruta_extraccion=path_descomprimir)


@app.route('/RNA', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        if not util.validar_archivo(request):
            redirect(request.url)

        if not zip.extraer():
            return jsonify({"response": "No se pudo descomprimir el archivo"})

        try:
            cargar_nuevos_chats()
        except Exception as e:
            return jsonify({"response": "No se pudo cargar los nuevos chats"})

        duration = 0
        try:
            start_time = time.time()
            train_model()
            end_time = time.time()
            duration = end_time - start_time
        except Exception as e:
            return jsonify({"response": "No se pudo entrenar el modelo"})

        response = "Modelo entrenado con exito en " + str(duration) + " segundos"
        return jsonify(
            {
                "response": response
            }
        )

    return render_template('index.html', **locals())


if __name__ == '__main__':
    print("*"*10, "Starting Train model service in port 8887")
    app.run(host='0.0.0.0', port='8887', debug=True)
