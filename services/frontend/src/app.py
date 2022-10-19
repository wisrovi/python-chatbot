import os
import shutil
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
    path_descomprimir = os.path.dirname(os.path.abspath(__file__)) + os.sep + "tmp" + os.sep
    print("Execution in: Local")
else:
    path_descomprimir = os.sep + "tmp" + os.sep
    print("Execution in: Docker")

if os.environ.get("SO") is None:
    path_poner_datos_para_entrenar = os.path.dirname(os.path.abspath(__file__)) + os.sep + "nuevos_chats" + os.sep
    print("Execution in: Local")
else:
    path_poner_datos_para_entrenar = os.sep + "nuevos_chats" + os.sep
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


@app.route('/upload', methods=["GET"])
def upload():
    return render_template('received_file0.html', **locals())


@app.route('/uploadData', methods=["GET", "POST"])
def upload_data():
    if request.method == 'POST':
        if not util.validar_credenciales(request):
            print("Credenciales incorrectas")
            return jsonify({"response": "Credenciales incorrectas"})

        if not util.validar_archivo(request):
            return jsonify({"response": "Archivo no valido"})

        directorios_temporales = os.listdir(path_descomprimir)
        for directorio in directorios_temporales:
            shutil.rmtree(os.path.join(path_descomprimir, directorio))

        if not zip.extraer():
            return jsonify({"response": "No se pudo descomprimir el archivo"})

        validacion_integridad = util.validar_integridad_archivos(path_descomprimir)
        if not validacion_integridad[0]:
            archivos_falla = validacion_integridad[1]
            problemas = list()
            for archivo in archivos_falla:
                file = archivo[0]
                problema = archivo[1]
                problemas.append(dict(folder=file, problem=problema))
            return jsonify(
                {
                    "fail_tags": problemas
                }
            )        
       
        """
        mover todos los archivos de la carpeta /tmp a la carpeta /nuevos_chats
        """
        contenidos = os.listdir(path_descomprimir)
        for contenido in contenidos:
            shutil.copytree(os.path.join(path_descomprimir, contenido), os.path.join(path_poner_datos_para_entrenar, contenido), dirs_exist_ok=True)
            shutil.rmtree(os.path.join(path_descomprimir, contenido), ignore_errors=True)

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
