import os
from flask import Flask, render_template, jsonify, request
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


@app.route('/RNA', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        # leyendo jsoo recibido
        json_received = request.get_json()
        if json_received is not None:
            if json_received["msg"] == "entrenar":
                duration = 0
                try:
                    start_time = time.time()
                    train_model()
                    end_time = time.time()
                    duration = end_time - start_time
                except Exception as e:
                    return jsonify({"response": "No se pudo entrenar el modelo"})

                response = "Modelo entrenado con exito en " + str(duration) + " segundos"

                # TODO: guardar un log de la fecha y hora de entrenamiento
                # TODO: guardar los tres ultmiros modelos entrenados

                return jsonify(
                    {
                        "response": response,
                        "status": 200
                    }
                )

        return jsonify(
            {
                "response": "No se pudo entrenar el modelo"
            }
        )

    return render_template('index.html', **locals())

# TODO: documentar los endpoints con swagger
# TODO: documentar el codigo con docstring y comentarios

if __name__ == '__main__':
    print("*"*10, "Starting Train model service in port 8887")
    app.run(host='0.0.0.0', port='8887', debug=True)
