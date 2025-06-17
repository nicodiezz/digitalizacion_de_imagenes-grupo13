from flask import Flask, request, render_template, url_for, flash, get_flashed_messages#, redirect

app = Flask(__name__)
app.secret_key = 'clave_secreta'

#Context Process
@app.context_processor
def messages():
    return get_flashed_messages(with_categories=True)

# Endpoints
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/process", methods=["POST"])
def process():
    image = request.files['image']
    if not image:
        flash('No image uploaded')
    #hacer algo y guardar en static/output,jpg
    return render_template('index.html')

@app.route("/upload", methods=["POST"])
def upload():
    image = request.files['image']
    if not image:
        flash('No image uploaded')
        return render_template('index.html')
    image.save(f'static/input.jpg')
    
    return render_template('index.html')
    


if __name__ == "__main__":
    app.run(debug=True)