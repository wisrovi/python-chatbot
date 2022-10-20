import os
from flask import Flask, render_template, jsonify, request
from src.libraries.train_bot import train_model
from src.libraries.Redis import start_conection
import time
import datetime

app = Flask(__name__)


if os.environ.get("SO") is None:
    filepath = os.path.dirname(os.path.abspath(__file__)) + os.sep + "received_files" + os.sep + "recibido.zip"
    path_descomprimir = os.path.dirname(os.path.abspath(__file__)) + os.sep + "nuevos_chats" + os.sep
    redis = start_conection(server="localhost", port=16379)
    print("Execution in: Local")
else:
    filepath = os.sep + "received_files" + os.sep + "recibido.zip"
    path_descomprimir = os.sep + "nuevos_chats" + os.sep
    redis = start_conection(server="redis", port=6379)
    print("Execution in: Docker")



"""
get version
"""
@app.route('/version', methods=["GET"])
def version():
    return jsonify({"version": "1.0.0"})


@app.route('/RNA', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        # leyendo jsoo recibido
        try:
            json_received = request.get_json()
        except Exception as e:
            form = request.form
            json_received = form.to_dict()

        if json_received is not None:
            if json_received["msg"] == "entrenar":
                duration = 0
                keys = history = None
                try:
                    start_time = time.time()
                    loss, accuracy = train_model()
                    end_time = time.time()
                    duration = end_time - start_time
                except Exception as e:
                    return jsonify({"response": "No se pudo entrenar el modelo"})

                response = "Modelo entrenado con exito en " + str(round(duration, 2)) + " segundos"

                # TODO: guardar un log de la fecha y hora de entrenamiento
                # TODO: guardar los tres ultmiros modelos entrenados

                redis.save("model_duration", str(round(duration, 2)) + " segundos")
                redis.save("model_loss", str(loss))
                redis.save("model_accuracy", str(accuracy))

                today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                redis.save("model_date", str(today))
                redis.crear_autoincremental("count_train")

                return jsonify(
                    {
                        "response": response,
                        "loss": loss,
                        "accuracy": accuracy,
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
