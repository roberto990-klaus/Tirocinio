document.addEventListener('DOMContentLoaded', function () {
    const formModificaDati = document.getElementById('formModificaDati');
    const errorAlert = document.getElementById('error-alert-modifica');
    const errorMessage = document.getElementById('error-message-modifica');
    const successAlert = document.getElementById('success-alert-modifica');
    const successMessage = document.getElementById('success-message-modifica');
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
                errorMessage.style.display = "none";
            }
        })
        .catch(error => console.error("Errore nella richiesta: ", error));
    });

    btnModificaDati.addEventListener('click', function () {
        errorAlert.style.display = 'none';
    });
});


document.addEventListener('DOMContentLoaded', function() {
    caricaDatiUtente();
});

function caricaDatiUtente() {
    // Effettua una richiesta AJAX per ottenere i dati dell'utente
    fetch('/dati_utente')
    .then(response => response.json())
    .then(data => {
        // Verifica se ci sono errori nella risposta
        if (data.error) {
            console.error(data.error);
        } else {
            // Visualizza i dati dell'utente nella pagina HTML
            document.getElementById('info-utente').innerHTML = `
                <h1 id="titolo_info_utente">User Information</h1><br>
                <p><strong id="nome_attuale">Nome:</strong> ${data.nome}</p>
                <p><strong id="cognome_attuale">Cognome:</strong> ${data.cognome}</p>
                <p><strong id="data_nascita_attuale">Data di Nascita:</strong> ${data.data_di_nascita}</p>
                <p><strong id="codice_fiscale_attuale">Codice Fiscale:</strong> ${data.cf}</p>
            `;
        }
    })
    .catch(error => {
        console.error('Si è verificato un errore durante il recupero dei dati dell\'utente:', error);
    });
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