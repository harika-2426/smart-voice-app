from flask import Flask, render_template, request, send_file
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
import os


app = Flask(__name__)


@app.route("/", methods=["GET","POST"])
def home():

    translation = ""
    audio_file = ""


    if request.method == "POST":

        text = request.form.get("text")

        source = request.form.get("source")

        target = request.form.get("target")


        try:

            translation = GoogleTranslator(
                source="auto" if source=="auto" else source,
                target=target
            ).translate(text)


            # create voice output

            speech = gTTS(
                text=translation,
                lang=target
            )

            audio_file = "translation.mp3"

            speech.save(
                "static/" + audio_file
            )


        except Exception as e:

            translation = "Error occurred"



    return render_template(
        "index.html",
        translation=translation,
        audio=audio_file
    )




@app.route("/voice")
def voice():

    recognizer = sr.Recognizer()


    with sr.Microphone() as source:

        audio = recognizer.listen(source)


    try:

        text = recognizer.recognize_google(audio)

        return text


    except:

        return "Could not understand"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)