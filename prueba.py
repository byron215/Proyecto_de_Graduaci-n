import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
import io

# Cargar el modelo previamente entrenado
model_path = 'C:/Users/anton/OneDrive/Escritorio/modelo/modelos.h5'
model = tf.keras.models.load_model(model_path)

# Parámetros de preprocesamiento de imágenes
img_height, img_width = 224, 224

# Crear la ventana principal
root = tk.Tk()
root.title("Clasificador de Imágenes Reciclables")
root.geometry("600x600")

# Función para cargar y preprocesar la imagen cargada
def classify_image():
    # Obtener la imagen cargada
    file_path = filedialog.askopenfilename(
        filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    )
    
    if not file_path:
        return

    # Cargar la imagen utilizando PIL (Python Imaging Library)
    img = Image.open(file_path)
    img = img.resize((img_height, img_width))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # Agregar una dimensión adicional para el lote

    # Realizar la predicción con el modelo
    prediction = model.predict(img_array)

    # Mostrar la imagen cargada
    img_tk = ImageTk.PhotoImage(img)
    label_image.config(image=img_tk)
    label_image.image = img_tk  # Para que la referencia no sea eliminada

    # Mostrar el resultado de la predicción
    if prediction[0][0] > 0.5:
        result = 'El producto de la imagen es reciclable.'
    else:
        result = 'El producto de la imagen no es reciclable.'
    
    messagebox.showinfo("Resultado de la predicción", result)

# Botón para cargar y clasificar la imagen
button_classify = tk.Button(root, text="Cargar Imagen y Clasificar", command=classify_image)
button_classify.pack(pady=20)

# Etiqueta para mostrar la imagen cargada
label_image = tk.Label(root)
label_image.pack()

# Ejecutar la ventana
root.mainloop()
