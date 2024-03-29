document.addEventListener('DOMContentLoaded', function () {
    const btnGeneraCodiceFiscale = document.getElementById('btnGeneraCodiceFiscale');
    const codiceFiscaleContainer = document.getElementById('codiceFiscaleContainer');
    const codiceFiscaleElement = document.getElementById('codiceFiscale');
    const errorGenerazioneCF = document.getElementById('error-generazione-cf');

    btnGeneraCodiceFiscale.addEventListener('click', function () {
        // Nascondi l'alert di errore all'inizio del tentativo di generare il codice fiscale
        errorGenerazioneCF.style.display = 'none';

        // Recupera i dati necessari dal form 
        const formData = new FormData(document.getElementById('formRegister'));

        // Effettua una richiesta fetch per ottenere il codice fiscale
        fetch("/generate_codice_fiscale", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Se la richiesta ha avuto successo e non ci sono errori
            if (!data.error) {
                // Mostra il codice fiscale nel container appropriato
                codiceFiscaleElement.textContent = data.codice_fiscale;
                codiceFiscaleContainer.style.display = 'block';
            } else {
                // Altrimenti, mostra l'alert di errore
                errorGenerazioneCF.style.display = 'block';
            }
        })
        .catch(error => console.error("Errore nella richiesta: ", error));
    });
});







