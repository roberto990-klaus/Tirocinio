$(document).ready(function() {
  $('form').submit(function(event) {
    event.preventDefault();

    var formData = new FormData($(this)[0]);

    $.ajax({
      url: '/predict',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function(response) {
        $('#prediction_result').text('Risultato della previsione: ' + response.prediction);
      },
      error: function(error) {
        console.log(error);
        $('#prediction_result').text('Errore nella previsione.');
      }
    });
  });
});



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

// Aggiunge un gestore di eventi al form per il caricamento dell'immagine
document.getElementById('imageForm').addEventListener('submit', function(event) {
  event.preventDefault();
  showSuccessAlert();
});