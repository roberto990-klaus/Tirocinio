import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def generate_heatmap_custom_colors(image_path, sigma=5):
    # Leggi l'immagine
    image = cv2.imread(image_path)

    # Converte l'immagine in scala di grigi
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Applica un filtro di Gauss all'immagine
    blurred_image = cv2.GaussianBlur(gray_image, (0, 0), sigma)

    # Crea una heatmap normalizzata
    heatmap = cv2.normalize(blurred_image, None, 0, 255, cv2.NORM_MINMAX)

    # Mappa i valori della heatmap su una scala di colori personalizzata
    heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)  # Usa COLORMAP_GIST_HEAT per verde e blu

    return heatmap_colored

def main():
    # Inserisci il percorso dell'immagine
    image_path = 'model/test_image2.jpeg'

    # Genera la heatmap
    heatmap_colored = generate_heatmap_custom_colors(image_path)

    # Mostra l'immagine originale e la heatmap colorata
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB))
    plt.title('Immagine originale')

    plt.subplot(1, 2, 2)
    plt.imshow(heatmap_colored)
    plt.title('Heatmap Colored')

    # Salva l'immagine nella cartella 'save_img'
    save_folder = 'save_img'
    os.makedirs(save_folder, exist_ok=True)  # Crea la cartella se non esiste
    save_path = os.path.join(save_folder, 'heatmap_colored_image.jpg')
    cv2.imwrite(save_path, cv2.cvtColor(heatmap_colored, cv2.COLOR_RGB2BGR))  # Converti il formato per OpenCV

    # Visualizza l'immagine salvata
    plt.figure()
    plt.imshow(heatmap_colored)
    plt.title('Heatmap Colored (Salvata)')
    plt.show()

if __name__ == "__main__":
    main()










