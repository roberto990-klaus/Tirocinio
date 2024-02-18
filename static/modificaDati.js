document.addEventListener('DOMContentLoaded', function () {
    const formModificaDati = document.getElementById('formModificaDati');
    const errorAlert = document.getElementById('error-alert');
    const errorMessage = document.getElementById('error-message');
    const successAlert = document.getElementById('success-alert');
    const successMessage = document.getElementById('success-message');
    const btnModificaDati = document.getElementById('btnModificaDati');

    formModificaDati.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(formModificaDati);

        fetch("/modifica_dati.html", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                errorMessage.textContent = data.error;
                errorAlert.style.display = "block";
            } else if (data.success) {
                successMessage.textContent = data.success;
                successAlert.style.display = "block";
                errorAlert.style.display = "none";
            }
        })
        .catch(error => console.error("Errore nella richiesta: ", error));
    });

    btnModificaDati.addEventListener('click', function () {
        errorAlert.style.display = 'none';
    });
});



// // Aggiungi un gestore di eventi per il modulo di caricamento dell'immagine
// document.getElementById("imageForm").addEventListener("submit", function(event) {
//     event.preventDefault();
//     var formData = new FormData(this);
//     fetch("/after_login.html", {
//         method: "POST",
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {
//         // Mostra l'immagine analizzata
//         var resultContainer = document.getElementById("resultContainer");
//         var resultImage = document.createElement("img");
//         resultImage.src = data.result_path;
//         resultContainer.appendChild(resultImage);
//     })
//     .catch(error => console.error("Errore durante il caricamento dell'immagine:", error));
// });