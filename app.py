
from flask import Flask, send_from_directory, request
import os

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/guardar', methods=['POST'])
def guardar():
    data = request.json
    nombre_archivo = data.get("archivo")
    contenido = data.get("contenido")
    if not nombre_archivo or contenido is None:
        return {"status": "error", "message": "Faltan datos"}, 400
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.route('/leer', methods=['GET'])
def leer():
    nombre_archivo = request.args.get("archivo")
    if not nombre_archivo or not os.path.exists(nombre_archivo):
        return {"status": "error", "message": "Archivo no encontrado"}, 404
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
        return {"status": "ok", "contenido": contenido}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
