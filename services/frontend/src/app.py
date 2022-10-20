import os
import shutil
from flask import Flask, render_template, jsonify, request, redirect
from libraries.processor import chatbot_response, solicitar_entrenamiento, \
    informar_nuevo_modelo, get_version_backend, get_version_training, \
        get_tags, get_intents
from libraries.UtilZipFile import UtilZipFile
from libraries.UtilReceivedFile import UtilReceivedFile
from libraries.cargar_nuevos_chats import cargar_nuevos_chats
from libraries.Redis import start_conection
import time
from flask_swagger import swagger


time.sleep(1)


app = Flask(__name__)

if os.environ.get("SO") is None:
    filepath = os.path.dirname(os.path.abspath(__file__)) + os.sep + "received_files" + os.sep + "recibido.zip"
    path_descomprimir = os.path.dirname(os.path.abspath(__file__)) + os.sep + "tmp" + os.sep
    path_poner_datos_para_entrenar = os.path.dirname(os.path.abspath(__file__)) + os.sep + "nuevos_chats" + os.sep
    redis = start_conection(server="localhost", port=16379)
    print("Execution in: Local")
else:
    filepath = os.sep + "received_files" + os.sep + "recibido.zip"
    path_descomprimir = os.sep + "tmp" + os.sep
    path_poner_datos_para_entrenar = os.sep + "nuevos_chats" + os.sep
    redis = start_conection(server="redis", port=6379)
    print("Execution in: Docker")


util = UtilReceivedFile(path_guardar_archivo_recibido=filepath, nombres_parametros={"zip": "file1"})
zip = UtilZipFile(filepath, ruta_extraccion=path_descomprimir)


# https://pypi.org/project/flask-swagger/
@app.route("/docs", methods=["GET"])
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0.0"
    swag['info']['title'] = "Chatbot API Uniongr"
    return jsonify(swag)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html', **locals())


"""
get version
"""
@app.route('/version', methods=["GET"])
def version():
    """
    Read version of backend, frontend and training
    ---
    tags:
        - version
    parameters:
        - name: version
    definitions:
        definitions:
          - schema:
              id: version
              properties:
                name:
                   type: string
                   description: version del proyecto
    responses:
        200:
            description: version del proyecto  
    """
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


# get tags from backend
@app.route('/tags', methods=["GET"])
def tags():
    tags = get_tags()
    return jsonify({"tags": tags})


# get intents from backend
@app.route('/intents', methods=["GET"])
def intents():
    intents = get_intents()
    return jsonify({"intents": intents})


# borrar un directorio de la carpeta nuevos_chats
@app.route('/del_tag', methods=["GET"])
def del_tag():
    """
    example: http://localhost:1037/del_tag?tag=tag1
    """
    tag = request.args.get('tag', default = "", type = str)
    if len(tag) > 0:
        path = os.path.join(path_poner_datos_para_entrenar, tag)
        print(f"borrar el directorio {path}")
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
            return jsonify({"response": "ok"})
        else:
            return jsonify({"response": "tag not found"})
    return jsonify({"response": "error"})


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

        rta, res_data = solicitar_entrenamiento()
        if rta[1] == 200:
            rta[1] = informar_nuevo_modelo()

        return jsonify({"response": res_data})

    return render_template('received_file.html', **locals())


# get last training
@app.route('/last_training', methods=["GET"])
def last_training():
    model_duration = redis.read("model_duration")
    model_loss = redis.read("model_loss")
    model_accuracy = redis.read("model_accuracy")
    model_date = redis.read("model_date")
    count_train = redis.read("count_train")
    return jsonify({
        "model_duration": model_duration,
        "model_loss": model_loss,
        "model_accuracy": model_accuracy,
        "model_date": model_date,
        "count_train": count_train
        })




# TODO: agregar un endpoint para que el frontend pueda consultar los tags que se encuentran 
# TODO: agrewgar un endpoint para que el frontend pueda limpia la carpeta 'nuevos_chats'
# TODO: agregar un endpoint para que el frontend pueda consultar el estado del entrenamiento
# TODO: agregar un endpoint para que el frontend pueda hacer un CRUD de los usuarios
# TODO: dcoumentar el codigo con docstrings y comentarios 
# TODO: documentar los endpoints con swagger

if __name__ == '__main__':
    print("Starting Frontend in port 8888")
    app.run(host='0.0.0.0', port='8888', debug=True)
