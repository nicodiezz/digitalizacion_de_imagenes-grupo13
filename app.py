from flask import Flask, request, render_template, flash, get_flashed_messages, send_file, redirect, url_for
from PIL import Image
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta'

INPUT_PATH = 'static/input.jpg'
OUTPUT_PATH = 'static/output.jpg'

@app.route("/")
def index():
    return render_template(
        'index.html',
        input_image=os.path.exists(INPUT_PATH),
        output_image=os.path.exists(OUTPUT_PATH)
    )

@app.route("/upload", methods=["POST"])
def upload():
    image = request.files.get('image')
    if not image:
        flash('No image uploaded', 'error')
        return render_template('index.html')
    image.save(INPUT_PATH)
    flash('Imagen cargada correctamente', 'success')
    return render_template('index.html', input_image=True, output_image=False)

@app.route("/process", methods=["POST"])
def process():
    if not os.path.exists(INPUT_PATH):
        flash("Primero subí una imagen", "error")
        return render_template("index.html", input_image=False, output_image=False)

    resolution = request.form.get("resolution")
    bit_depth = request.form.get("bit_depth")

    allowed_resolutions = {"100x100", "500x500", "1000x1000"}
    if resolution not in allowed_resolutions:
        flash(f"Resolución no válida: {resolution}", "error")
        return render_template("index.html", input_image=True, output_image=False)

    try:
        bit_depth = int(bit_depth)
        if bit_depth not in {1, 8, 24}:
            raise ValueError()
    except:
        flash("Profundidad de bits inválida", "error")
        return render_template("index.html", input_image=True, output_image=False)

    img = Image.open(INPUT_PATH)
    width, height = map(int, resolution.split('x'))
    img = img.resize((width, height), Image.LANCZOS)

    if bit_depth == 1:
        img = img.convert("1")
    elif bit_depth == 8:
        img = img.convert("L")
    elif bit_depth == 24:
        img = img.convert("RGB")

    img.save(OUTPUT_PATH, format="JPEG", quality=70)

    flash("Imagen digitalizada exitosamente", "success")
    return render_template("index.html", input_image=True, output_image=True)

@app.route("/compress", methods=["POST"])
def compress():
    if not os.path.exists(INPUT_PATH):
        flash("Primero subí una imagen para comprimir", "error")
        return render_template("index.html", input_image=False, output_image=False)

    img = Image.open(INPUT_PATH)
    img.save(OUTPUT_PATH, format="JPEG", quality=40)

    return redirect(url_for("download"))

@app.route("/download", methods=["GET"])
def download():
    if not os.path.exists(OUTPUT_PATH):
        flash("No hay imagen para descargar", "error")
        return render_template("index.html", input_image=os.path.exists(INPUT_PATH), output_image=False)

    return send_file(OUTPUT_PATH, as_attachment=True, download_name="imagen_comprimida.jpg")

@app.route("/clear", methods=["POST"])
def clear():
    if os.path.exists(INPUT_PATH):
        os.remove(INPUT_PATH)
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)
    flash("Imágenes eliminadas correctamente", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
