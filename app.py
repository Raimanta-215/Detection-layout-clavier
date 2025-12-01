from flask import Flask, render_template, request, send_from_directory
import os
from src.traitement_image.mon_traitement import traiter_image_fichier

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

IMAGE_SAVE_PATH = os.path.join(BASE_DIR, "images")
os.makedirs(IMAGE_SAVE_PATH, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    image_file = request.files["image"]

    input_path = os.path.join(IMAGE_SAVE_PATH, "input.jpg")
    output_path = os.path.join(IMAGE_SAVE_PATH, "processed.jpg")

    image_file.save(input_path)

    
    success, message = traiter_image_fichier(input_path, output_path)

    return render_template(
        "processed.html",
        result=message,
        processed_image="/images/processed.jpg" if success else None
    )


@app.route("/images/<path:filename>")
def images(filename):
    return send_from_directory(IMAGE_SAVE_PATH, filename)


if __name__ == "__main__":
    app.run(debug=True)
