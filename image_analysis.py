import os
from flask import send_from_directory, request, redirect, flash, jsonify
from heatmap import generate_grad_cam, generate_heatmap_custom_colors
from model.classification_utils import load_model
from werkzeug.utils import secure_filename

# Carica il modello una sola volta quando il modulo viene caricato
model_data = load_model()
model = model_data['model']
class_names = model_data['class_names']

# Aggiungi questa funzione per eseguire l'analisi dell'immagine
def analyze_image(app_root):
    # Controlla se è stata inviata un'immagine
    if 'file' not in request.files:
        flash('Nessun file selezionato')
        return redirect(request.url)

    file = request.files['file']

    # Controlla se il file ha un nome
    if file.filename == '':
        flash('Nessun file selezionato')
        return redirect(request.url)

    # Crea la cartella temporanea se non esiste
    temp_dir = os.path.join(app_root, 'save_img', 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    # Salva il file nella cartella temporanea
    file_path = os.path.join(temp_dir, file.filename)
    file.save(file_path)

    # Esegui l'analisi dell'immagine
    try:
        grad_cam, predicted_class_name = generate_grad_cam(model_data, file_path, 'conv2d_2')
        heatmap_colored = generate_heatmap_custom_colors(grad_cam)
    except Exception as e:
        flash(f'Errore durante l\'analisi dell\'immagine: {str(e)}')
        return redirect(request.url)

    # Restituisci il percorso dell'immagine analizzata
    return {"image_path": file_path}
