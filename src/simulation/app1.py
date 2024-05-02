from flask import Flask, render_template
from src.LM import procesar_y_generar_comentarios

app = Flask(__name__)

@app.route('/ejecutar_funcion')
def ejecutar_funcion():
    resultado = procesar_y_generar_comentarios('salida.txt')
    return resultado

@app.route('/')
def index():
    return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True)