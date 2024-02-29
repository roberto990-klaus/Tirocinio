document.addEventListener('DOMContentLoaded', function () {
    const formEliminazione = document.getElementById('formEliminazione');
    const errorAlert = document.getElementById('error-alert-elimina');
    const errorMessage = document.getElementById('error-message-elimina');
    const successAlert = document.getElementById('success-alert-elimina');
    const successMessage = document.getElementById('success-message-elimina');

    formEliminazione.addEventListener('submit', function (e) {
        e.preventDefault(); // Impedisce il reindirizzamento predefinito del modulo

        const formData = new FormData(formEliminazione);

        fetch("/elimina_dati.html", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                errorMessage.textContent = data.error;
                errorAlert.style.display = "block";
                successAlert.style.display = "none"; // Assicurati che l'alert di successo sia nascosto
            } else if (data.success) {
                successMessage.textContent = data.success;
                successAlert.style.display = "block";
                errorAlert.style.display = "none"; // Assicurati che l'alert di errore sia nascosto
            }
            setTimeout(function() {
                window.location.href = "/login.html";
            }, 4000);
        })
        .catch(error => console.error("Errore nella richiesta: ", error));
    });
});


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
