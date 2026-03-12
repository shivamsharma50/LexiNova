from flask import Flask, render_template, request, jsonify
from groq import Groq
from langdetect import detect

app = Flask(__name__)

client = Groq(api_key="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")
def translate_text(text, target_language):

    try:
        detected_language = detect(text)
    except:
        detected_language = "unknown"

    prompt = f"""
Detected language: {detected_language}
Translate the following text into {target_language}.
Return only the translated text.
Text:
{text}
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    translated = response.choices[0].message.content.strip()
    return translated, detected_language
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    text = data["text"]
    target_language = data["target_language"]
    translated, detected = translate_text(text, target_language)
    return jsonify({
        "translated_text": translated,
        "detected_language": detected
    })
@app.route("/translate-file", methods=["POST"])
def translate_file():
    file = request.files["file"]
    target_language = request.form.get("target_language")
    if file.filename.endswith(".txt"):
        text = file.read().decode("utf-8")
        translated, detected = translate_text(text, target_language)
        return jsonify({
            "translated_text": translated,
            "detected_language": detected
        })
    return jsonify({
        "translated_text": "Only TXT files supported"
    })
if __name__ == "__main__":
    app.run(debug=True)