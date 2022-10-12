import os
from flask import Flask, render_template, jsonify, request, redirect
from libraries.processor import chatbot_response, solicitar_entrenamiento, informar_nuevo_modelo
from libraries.UtilZipFile import UtilZipFile
from libraries.UtilReceivedFile import UtilReceivedFile
from libraries.cargar_nuevos_chats import cargar_nuevos_chats

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


@app.route('/chatbot', methods=["POST"])
def chatbotResponse():
    the_question = request.form['question']
    response = chatbot_response(the_question)

    return jsonify({"response": response})


@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        if not util.validar_archivo(request):
            redirect(request.url)

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


if __name__ == '__main__':
    print("Starting Frontend in port 8888")
    app.run(host='0.0.0.0', port='8888', debug=True)
