// Aggiungi un gestore di eventi per il modulo di caricamento dell'immagine
document.getElementById("imageForm").addEventListener("submit", function(event) {
  event.preventDefault();
  var formData = new FormData(this);
  fetch("/after_login.html", {
      method: "POST",
      body: formData
  })
  .then(response => response.json())
  .then(data => {
      // Mostra l'immagine analizzata
      var resultContainer = document.getElementById("resultContainer");
      var resultImage = document.createElement("img");
      resultImage.src = data.result_path;
      resultContainer.appendChild(resultImage);
  })
  .catch(error => console.error("Errore durante il caricamento dell'immagine:", error));
});



// Funzione per mostrare l'alert verde quando si clicca su "Carica immagine"
function showSuccessAlert() {
  var successAlert = document.getElementById('success-alert-carica');
  successAlert.style.display = 'block';
  // Nasconde l'alert dopo 5 secondi
  setTimeout(function() {
      successAlert.style.display = 'none';
  }, 5000);
}

// Aggiungi un gestore di eventi al form per il caricamento dell'immagine
document.getElementById('imageForm').addEventListener('submit', function(event) {
  event.preventDefault();
  showLoadingAnimation(); // Mostra l'animazione di caricamento

  // Simula il caricamento dell'immagine (sostituire con la tua logica di caricamento effettiva)
  setTimeout(function() {
      document.getElementById('loading-progress').style.width = '100%'; // Completa la barra di caricamento
      setTimeout(function() {
          showSuccessAlert(); // Mostra l'alert di successo dopo la barra di caricamento
          hideLoadingAnimation(); // Nasconde l'animazione di caricamento dopo l'alert di successo
      }, 2200); // Mostra l'alert di successo dopo circa 2,2 secondi
  }, 100); // Simulazione di un caricamento (100 millisecondi)

  var formData = new FormData(this);
  fetch("/after_login.html", {
      method: "POST",
      body: formData
  })
  .then(response => response.json())
  .then(data => {
      // Mostra l'immagine analizzata
      var resultContainer = document.getElementById("resultContainer");
      var resultImage = document.createElement("img");
      resultImage.src = data.result_path;
      resultContainer.appendChild(resultImage);
  })
  .catch(error => console.error("Errore durante il caricamento dell'immagine:", error));
});

// Funzione per mostrare l'alert verde quando si clicca su "Carica immagine"
function showSuccessAlert() {
  var successAlert = document.getElementById('success-alert-carica');
  successAlert.style.display = 'block';
  // Nasconde l'alert dopo 5 secondi
  setTimeout(function() {
      successAlert.style.display = 'none';
  }, 5000);
}



// Funzione per mostrare l'animazione di caricamento
function showLoadingAnimation() {
    var loadingSpinner = document.getElementById('loading-spinner');
    loadingSpinner.style.display = 'block';
}

// Funzione per nascondere l'animazione di caricamento
function hideLoadingAnimation() {
    var loadingSpinner = document.getElementById('loading-spinner');
    loadingSpinner.style.display = 'none';
}





document.addEventListener('DOMContentLoaded', function() {
  // Seleziona il menu di navigazione
  var navMenu = document.querySelector('.barra_navigazione');

  // Registra un listener per l'evento di scroll della finestra
  window.addEventListener('scroll', function() {
      // Calcola la posizione della finestra rispetto alla cima della pagina
      var scrollPosition = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;

      // Calcola la posizione a cui il menu dovrebbe scomparire, ad esempio 1/4 dell'altezza della finestra
      var hidePosition = window.innerHeight / 7;

      // Controlla se la posizione di scorrimento è oltre la posizione in cui il menu dovrebbe scomparire
      if (window.innerWidth <= 768 && scrollPosition > hidePosition) {
          // Nascondi il menu solo per schermi con larghezza inferiore o uguale a 768px
          navMenu.style.display = 'none';
      } else {
          // Altrimenti, mostra il menu settando la proprietà display a 'block'
          navMenu.style.display = 'block';
      }
  });

  // Registra un listener per l'evento di scroll della finestra
  window.addEventListener('scroll', function() {
      var languageContainer = document.getElementById('language-buttons-container');
      // Nascondi il contenitore dei pulsanti per la lingua solo per schermi con larghezza inferiore o uguale a 768px
      if (window.innerWidth <= 768 && window.scrollY > 100) {
          languageContainer.style.display = 'none';
      } else {
          // Altrimenti, mostra il contenitore dei pulsanti per la lingua
          languageContainer.style.display = 'block';
      }
  });
});
