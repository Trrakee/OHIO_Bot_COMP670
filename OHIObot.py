import os

from autocorrect import spell
from flask import Flask, render_template, request

import aiml_package

app = Flask(__name__)

BRAIN_FILE = "pretrained_model/pretrainedModel.dump"
k = aiml_package.Kernel()

if os.path.exists(BRAIN_FILE):
    print("Loading from brain file: " + BRAIN_FILE)
    k.loadBrain(BRAIN_FILE)
else:
    print("Parsing aiml_package files")
    k.bootstrap(learnFiles="pretrained_model/learningFileList.aiml_package", commands="load aiml_package")
    print("Saving brain file: " + BRAIN_FILE)
    k.saveBrain(BRAIN_FILE)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/get")
def get_bot_response():
    query = request.args.get('msg')
    query = [spell(w) for w in (query.split())]
    question = " ".join(query)
    response = k.respond(question)
    if response:
        return str(response)
    else:
        return str(":)")


if __name__ == "__main__":
    # app.run()
    app.run(host='127.0.0.1', port='8080', debug=False)
