from flask import Flask, request, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)


english_bot = ChatBot("MyChatBot",
                      storage_adapter="chatterbot.storage.SQLStorageAdapter",
                      database_uri='sqlite:///database.db',
                      # logic_adapters=[
                      #     'chatterbot.logic.MathematicalEvaluation',
                      #     'chatterbot.logic.TimeLogicAdapter',
                      #     'chatterbot.logic.BestMatch'
                      # ]
                      )
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("chatterbot.corpus.english")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(english_bot.get_response(userText))


@app.route("/get_api")
def bot_get():
    try:
        req_body = request.get_json('msg')
        bot_response = english_bot.get_response(req_body["msg"])
        return {"Bot_Response": f"{bot_response}"}, 200
    except Exception as e:
        return {"ERROR": "Error in get route: " + e}, 500


if __name__ == '__main__':
    app.run(debug=True)
