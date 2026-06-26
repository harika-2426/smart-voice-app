from flask import Flask, render_template, request
from deep_translator import GoogleTranslator
from gtts import gTTS

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

            speech = gTTS(text=translation, lang=target)
            audio_file = "translation.mp3"
            speech.save("static/" + audio_file)

        except:
            translation = "Error occurred"

    return render_template("index.html", translation=translation, audio=audio_file)


@app.route("/voice")
def voice():
    return "Voice input not supported on cloud."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)