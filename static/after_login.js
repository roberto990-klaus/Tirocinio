// Aggiungi un gestore di eventi al form per il caricamento dell'immagine
document.getElementById('imageForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Controlla se è stata selezionata un'immagine
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];
    if (!file) {
        showSelectImageError();
        return;
    }

    // Controlla l'estensione dell'immagine
    var allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
    if (!allowedExtensions.exec(file.name)) {
        showInvalidExtensionError();
        return;
    }

    // Caricamento dell'immagine
    showLoadingAnimation(); // Mostra l'animazione di caricamento

    // Simula il caricamento dell'immagine
    setTimeout(function() {
        document.getElementById('loading-progress').style.width = '100%'; // Completa la barra di caricamento
        setTimeout(function() {
            showSuccessAlert(); // Mostra l'alert di successo
            hideLoadingAnimation(); // Nasconde l'animazione di caricamento dopo l'alert di successo
        }, 2500); // Mostra l'alert di successo dopo 2,5 secondi
    }, 100); // Simulazione di un caricamento (100 millisecondi)

    // Simulazione di un caricamento (2,5 secondi)
    var formData = new FormData(this);
    setTimeout(function() {
        fetch("/after_login.html", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Mostra l'immagine analizzata solo se l'analisi ha avuto successo
            var resultContainer = document.getElementById("resultContainer");
            var resultImage = document.createElement("img");
            resultImage.src = data.result_path;
            resultContainer.appendChild(resultImage);
        })
        .catch(error => {
            // Se si verifica un errore durante il caricamento dell'immagine, mostra l'alert di errore
            console.error("Errore durante il caricamento dell'immagine:", error);
            showGenericError(); // Mostra l'alert di errore generico
        })
        .finally(() => {
            // Nasconde l'animazione di caricamento alla fine del caricamento, indipendentemente dall'esito
            hideLoadingAnimation();
        });
    }, 2500); // Simulazione di un caricamento (2,5 secondi)
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



// Funzione per mostrare l'alert di errore se nessuna immagine è stata selezionata
function showSelectImageError() {
    var errorMessage = document.getElementById('error-message-select-image');
    showErrorAlertImage(errorMessage);
}

// Funzione per mostrare l'alert di errore se l'estensione dell'immagine non è valida
function showInvalidExtensionError() {
    var errorMessage = document.getElementById('error-message-invalid-extension');
    showErrorAlertFormat(errorMessage);
}




// Funzione per mostrare l'alert di errore
function showErrorAlertImage() {
    var errorAlert = document.getElementById('error-alert-carica');
    errorAlert.style.display = 'block';
    // Nasconde l'alert dopo 3 secondi
    setTimeout(function() {
        errorAlert.style.display = 'none';
    }, 3000);
}

// Funzione per mostrare l'alert di errore
function showErrorAlertFormat() {
    var errorAlert = document.getElementById('error-alert-invalid-format');
    errorAlert.style.display = 'block';
    // Nasconde l'alert dopo 3 secondi
    setTimeout(function() {
        errorAlert.style.display = 'none';
    }, 3000);
}



// JavaScript per gestire il menu burger
function toggleMobileMenu() {
    var mobileMenu = document.getElementById("mobileMenu");
    mobileMenu.classList.toggle("show"); // Mostra o nasconde il menu a tendina
}

// JavaScript per chiudere il menu a tendina quando si clicca fuori da esso
window.onclick = function(event) {
    if (!event.target.matches('.burger-menu')) {
        var mobileMenu = document.getElementById("mobileMenu");
        if (mobileMenu.classList.contains('show')) {
            mobileMenu.classList.remove('show');
        }
    }
};
