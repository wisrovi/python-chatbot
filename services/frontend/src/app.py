import os
from flask import Flask, render_template, jsonify, request, redirect
from libraries.processor import chatbot_response, solicitar_entrenamiento, informar_nuevo_modelo, get_version_backend, get_version_training
from libraries.UtilZipFile import UtilZipFile
from libraries.UtilReceivedFile import UtilReceivedFile
from libraries.cargar_nuevos_chats import cargar_nuevos_chats
import time


time.sleep(1)


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


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html', **locals())


"""
get version
"""
@app.route('/version', methods=["GET"])
def version():
    version_frontend = "1.0.0"
    version_backend = get_version_backend()
    version_train_model = get_version_training()
    return jsonify({
        "version_front": version_frontend,
        "version_backend": version_backend,
        "version_train_model": version_train_model
        })


@app.route('/chatbot', methods=["POST"])
def chatbotResponse():
    the_question = request.form['question']
    response, tag = chatbot_response(the_question)

    if os.environ.get("DEBUG") is not None:
        response = f"({tag}) - {response}"

    return jsonify({"response": response})


@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        # TODO: pedir un login para poder subir archivos

        if not util.validar_archivo(request):
            redirect(request.url)

        # TODO: extraer el archivo en una carpeta temporal
        # TODO: validar que el archivo tenga la estructura correcta
        # TODO: validar que los archivos esten completos y no haya tags repetidos o vacios o incompletos
        # TODO: mover los archivos a la carpeta 'nuevos_chats'

        if not zip.extraer():
            return jsonify({"response": "No se pudo descomprimir el archivo"})

        try:
            cargar_nuevos_chats()
        except Exception as e:
            return jsonify({"response": "No se pudo cargar los nuevos chats"})

        rta = list(solicitar_entrenamiento())
        if rta[1] == 200:
            rta[1] = informar_nuevo_modelo()

        return jsonify({"response": rta})

    return render_template('received_file.html', **locals())


# TODO: agregar un endpoint para que el frontend pueda consultar los tags que se encuentran 
# TODO: agrewgar un endpoint para que el frontend pueda limpia la carpeta 'nuevos_chats'
# TODO: agregar un endpoint para que el frontend pueda consultar el estado del entrenamiento
# TODO: agregar un endpoint para que el frontend pueda hacer un CRUD de los usuarios
# TODO: dcoumentar el codigo con docstrings y comentarios 
# TODO: documentar los endpoints con swagger

if __name__ == '__main__':
    print("Starting Frontend in port 8888")
    app.run(host='0.0.0.0', port='8888', debug=True)
