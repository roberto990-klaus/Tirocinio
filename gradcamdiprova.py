import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from model.classification_utils import load_model, predict, load_image
from PIL import Image
from datetime import datetime

# Inizializzazione del modello
model_data = load_model()
model = model_data['model']
class_names = model_data['class_names']

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Funzione per generare la heatmap colorata
def generate_heatmap_custom_colors(image, sigma=5):
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (0, 0), sigma)
    heatmap = cv2.normalize(blurred_image, None, 0, 255, cv2.NORM_MINMAX)
    heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    return heatmap_colored





def generate_grad_cam(model, image_path, layer_name, sigma=5, transparency_factor=0.8):
    # Carica l'immagine e la pre-elabora
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (model['img_dim'], model['img_dim']))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)

    # Estrai la classe predetta e le probabilità
    class_probabilities = predict(model['model'], image, model['class_names'])
    predicted_class = np.argmax(class_probabilities)
    predicted_class_name = model['class_names'][predicted_class]

    # Trova il layer desiderato nel modello
    target_layer = model['model'].get_layer(layer_name)
    if target_layer is None:
        raise ValueError("Layer specificato non trovato nel modello.")

    # Crea un modello con input l'immagine e output il layer target
    heatmap_model = tf.keras.models.Model(model['model'].inputs, [target_layer.output, model['model'].output])

    # Calcola Grad-CAM
    with tf.GradientTape() as tape:
        conv_output, predictions = heatmap_model(image)
        class_idx = tf.argmax(predictions[0])  # Ottieni l'indice della classe predetta
        loss = predictions[:, class_idx]

    grads = tape.gradient(loss, conv_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    last_conv_layer_output = conv_output[0]
    heatmap = tf.reduce_mean(tf.multiply(last_conv_layer_output, pooled_grads), axis=-1)
    heatmap = tf.nn.relu(heatmap)
    heatmap /= tf.reduce_max(heatmap)

    heatmap = heatmap.numpy()
    heatmap = cv2.resize(heatmap, (image.shape[2], image.shape[1]))
    heatmap = cv2.GaussianBlur(heatmap, (sigma, sigma), 0)
    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    heatmap = np.uint8(heatmap)

    heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # Combinazione lineare pesata tra l'immagine originale e l'heatmap colorato
    grad_cam = cv2.addWeighted(cv2.convertScaleAbs(image[0]), 1 - transparency_factor, heatmap_colored, transparency_factor, 0)

    return grad_cam, predicted_class_name






def generate_heatmap(image_path):
    layer_name = 'conv2d_2'
    grad_cam, predicted_class_name = generate_grad_cam(model_data, image_path, layer_name)
    img = load_image(image_path, model_data['channels'], resize=model_data['img_dim'])
    pred = predict(model_data['model'], img, model_data['class_names'])
    heatmap_colored = generate_heatmap_custom_colors(grad_cam)
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y_%H-%M")
    plot_file = f'Immagine analizzata {timestamp}.jpg' 
    plot_path = os.path.join('static/save_img', plot_file)

    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB))
    plt.title(f'{pred} - 100.0%')

    plt.subplot(1, 3, 2)
    plt.imshow(heatmap_colored)
    plt.title('Heatmap')

    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(grad_cam, cv2.COLOR_BGR2RGB))
    plt.title('Overlay with Heatmap - Grad-CAM')

    plt.savefig(plot_path)
    plt.close()

    return plot_path, pred

def get_image_info(image_path, previsione):
    creation_time = os.path.getctime(image_path)
    creation_timestamp = datetime.fromtimestamp(creation_time).strftime("%d-%m-%Y,  %H:%M:%S")
    print("Creation timestamp from generate_heatmap():", creation_timestamp)
    return creation_timestamp, previsione