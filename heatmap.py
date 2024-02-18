import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from model.classification_utils import load_model, predict
from PIL import Image
from datetime import datetime



# Inizializzaziione del modello
model_data = load_model()
model = model_data['model']
class_names = model_data['class_names']

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Funzione per generare la heatmap colorata
def generate_heatmap_custom_colors(image, sigma=5):

    # Converte l'immagine in scala di grigi
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Applica un filtro di Gauss all'immagine
    blurred_image = cv2.GaussianBlur(gray_image, (0, 0), sigma)

    # Crea una heatmap normalizzata
    heatmap = cv2.normalize(blurred_image, None, 0, 255, cv2.NORM_MINMAX)

    # Mappa i valori della heatmap su una scala di colori personalizzata
    heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    return heatmap_colored



def generate_grad_cam(model, image_path, layer_name, sigma=5):

    # Carica l'immagine e la pre-processa
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (model['img_dim'], model['img_dim']))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)

    # Estrai il nome della classe predetta e le probabilità del modell addestrato
    class_probabilities = predict(model['model'], image, model['class_names'])
    predicted_class = np.argmax(class_probabilities)
    predicted_class_name = model['class_names'][predicted_class]

    # Trova il layer desiderato nel modello e verifica se è presente nel modello addestrato
    target_layer = model['model'].get_layer(layer_name)
    if target_layer is None:
        raise ValueError("Layer specificato non trovato nel modello.")

    # Crea un modello con l'input dell'immagine e l'output del layer target
    heatmap_model = tf.keras.models.Model(model['model'].inputs, [target_layer.output, model['model'].output])

    # Calcola il gradiente rispetto all'output del layer target rispetto all'input dell'immagine
    with tf.GradientTape() as tape:
        conv_output, predictions = heatmap_model(image)
        loss = predictions[:, predicted_class]

    grads = tape.gradient(loss, conv_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    heatmap = tf.reduce_mean(tf.multiply(pooled_grads, conv_output), axis=-1)
    heatmap = tf.nn.relu(heatmap)  # Applica ReLU per evidenziare solo i punti critici
    heatmap /= tf.reduce_max(heatmap)  # Normalizza la heatmap prima di convertirla in arraty

    heatmap = heatmap.numpy()[0]  # Converti in array numpy

    # Ridimensiona la heatmap per abbinarla alle dimensioni dell'immagine originale
    heatmap = cv2.resize(heatmap, (image.shape[2], image.shape[1]))

    # Applica un filtro di Gauss alla heatmap
    heatmap = cv2.GaussianBlur(heatmap, (sigma, sigma), 0)

    # Normalizza la heatmap
    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)

    # Mappa i valori della heatmap su una scala di colori personalizzata
    heatmap = np.uint8(255 * heatmap)
    # Aggiungi una dimensione per diventare un'immagine in scala di grigi
    heatmap = np.expand_dims(heatmap, axis=-1)  
    heatmap_colored = cv2.applyColorMap(heatmap[:, :, 0], cv2.COLORMAP_JET)

    # Calcola Grad-CAM sovrapponendo l'heatmap sull'immagine originale
    heatmap_resized = cv2.resize(np.array(heatmap_colored), (image.shape[2], image.shape[1]))
    grad_cam = cv2.addWeighted(np.uint8(255 * image[0]), 0.9, heatmap_resized, 0.1 , 0)

    return grad_cam, predicted_class_name

def generate_heatmap(image_path):
    # Scegli il layer desiderato (scelto a caso dopo la verifica di quali layer sono disponibili)
    layer_name = 'conv2d_2'

    # Genera Grad-CAM e ottieni il nome della classe predetta dal modello addestrato
    grad_cam, predicted_class_name = generate_grad_cam(model_data, image_path, layer_name)

    # Genera la heatmap
    heatmap_colored = generate_heatmap_custom_colors(grad_cam)

    # Salva il plot come immagine con la data e l'ora correnti come parte del nome del file per fare la ricerca nella datatable
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y_%H-%M")
    plot_file = f'Immagine analizzata {timestamp}.jpg' 
    plot_path = os.path.join('static/save_img', plot_file)

    
    # Salva il plot come immagine e visualizza le 3 immagini in serie
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB))
    plt.title(f'{predicted_class_name} - 100.0%')

    plt.subplot(1, 3, 2)
    plt.imshow(heatmap_colored)
    plt.title('Heatmap')

    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(grad_cam, cv2.COLOR_BGR2RGB))
    plt.title('Overlay with Heatmap - Grad-CAM')

    plt.savefig(plot_path)
    plt.close()
    
    return plot_path


def get_image_info(image_path):
    # Scegli il layer desiderato (scelto a caso dopo la verifica di quali layer sono disponibili)
    layer_name = 'conv2d_2'

    # Genera Grad-CAM e ottieni il nome della classe predetta dal modello addestrato
    _, predicted_class_name = generate_grad_cam(model_data, image_path, layer_name)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", predicted_class_name)

    # Ottieni la data e l'ora di creazione dell'immagine
    creation_time = os.path.getctime(image_path)
    creation_timestamp = datetime.fromtimestamp(creation_time).strftime("%d-%m-%Y,  %H:%M:%S")

    print("Creation timestamp from generate_heatmap():", creation_timestamp)

    return creation_timestamp, predicted_class_name
































# @app.route("/after_login.html", methods=["GET", "POST"])
# def after_login():
#     if request.method == "POST":
#         # Controlla se l'utente è loggato
#         if 'email_utente' not in session:
#             flash('Effettua il login prima di caricare un\'immagine')
#             return redirect(url_for('login_page'))

#         if 'file' not in request.files:
#             flash('Nessun file selezionato')
#             return redirect(request.url)

#         file = request.files['file']
#         if file.filename == '':
#             flash('Nessun file selezionato')
#             return redirect(request.url)

#         try:
#             # Salva il file temporaneo
#             temp_dir = os.path.join(app.root_path, 'temp')
#             os.makedirs(temp_dir, exist_ok=True)
#             temp_file_path = os.path.join(temp_dir, secure_filename(file.filename))
#             file.save(temp_file_path)

#             # Genera il plot e ottieni il percorso del file di plot
#             plot_path = generate_heatmap(temp_file_path)

#             # Rimuovi il file temporaneo dopo l'elaborazione
#             os.remove(temp_file_path)

#             # Leggi l'immagine come dati binari
#             with open(plot_path, "rb") as img_file:
#                 img_data = img_file.read()

#             # Recupera l'email dell'utente loggato
#             email_utente = session.get('email_utente')

#             # Salva l'immagine convertita nel database associata all'utente loggato
#             cursore.execute("INSERT INTO immagini_utenti (immagine, email_utente) VALUES (%s, %s)", (img_data, email_utente))
#             db_connessione.commit()

#             print("Immagine salvata nel database per l'utente:", email_utente)

#             return send_file(plot_path, mimetype='image/jpeg')

#         except Exception as e:
#             flash(f'Errore durante l\'analisi dell\'immagine: {str(e)}')
#             return redirect(request.url)

#     return render_template('after_login.html')
