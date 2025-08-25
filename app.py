from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from PIL import Image
import os
import uuid

app = Flask(__name__)


from flask import send_from_directory

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')


# Folder to save uploads
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]

        if file.filename == "":
            return "No selected file"

        if file and allowed_file(file.filename):
            width = int(request.form.get("width", 0))
            height = int(request.form.get("height", 0))
            filetype = request.form.get("filetype", "png")

            filename = str(uuid.uuid4()) + "." + filetype
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            img = Image.open(file)
            if width > 0 and height > 0:
                img = img.resize((width, height))

            img.save(filepath)

            # Get file size in KB
            size_kb = round(os.path.getsize(filepath) / 1024, 2)

            return render_template(
                "index.html",
                filename=filename,
                width=width,
                height=height,
                size=size_kb
            )

    return render_template("index.html", filename=None)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
