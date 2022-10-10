from flask import Flask, render_template, jsonify, request
import processor


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html', **locals())



@app.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():
    if request.method == 'POST':
        the_question = request.form['question']
        response = processor.chatbot_response(the_question)

    return jsonify({"response": response })



if __name__ == '__main__':
    print("Starting Frontend in port 8888")
    app.run(host='0.0.0.0', port='8888', debug=True)
