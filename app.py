from flask import Flask, request, render_template, redirect, url_for, session
import numpy as np
import tensorflow as tf
from PIL import Image
import io
import base64

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesaria para usar sesiones

# Cargar el modelo entrenado
model = tf.keras.models.load_model(r'C:\Users\anton\OneDrive\Escritorio\modelo\mmoddeelloos.h5')

# Credenciales de ejemplo
USERNAME = 'usuario'
PASSWORD = 'contraseña'

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('conte'))  # Redirige a la página principal si las credenciales son correctas
        else:
            error = 'Credenciales incorrectas. Intenta de nuevo.'
            return render_template('login.html', error=error)
    return render_template('login.html')

# Ruta principal que renderiza la página HTML
@app.route('/')
def conte():
    if not session.get('logged_in'):
        return redirect(url_for('login'))  # Si no ha iniciado sesión, redirige a la página de login
    return render_template('conte.html')

# Ruta para procesar la imagen y realizar la predicción
@app.route('/predict', methods=['POST'])
def predict():
    if not session.get('logged_in'):
        return redirect(url_for('login'))  # Verifica si el usuario está autenticado
    file = request.files['image']
    img = Image.open(file)
    img_array = preprocess_image(img)
    
    prediction = model.predict(img_array)
    if prediction[0][0] > 0.5:
        result = 'El producto de la imagen es reciclable.'
    else:
        result = 'El producto de la imagen no es reciclable.'
    
    # Convertir la imagen a base64 para mostrarla en la página
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode()

    return render_template('index.html', result=result, image_data=img_base64)

# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/conte')
def conte_page():
    return render_template('conte.html')

@app.route('/ana')
def conte_pages():
    return render_template('index.html')

@app.route('/noso')
def conte_pagees():
    return render_template('noso.html')

# Función para preprocesar la imagen
def preprocess_image(image):
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

if __name__ == '__main__':
    app.run(debug=True)
