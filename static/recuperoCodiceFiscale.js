// Script per recuperare il codice fiscale dal file python 
document.addEventListener('DOMContentLoaded', function () {
    const btnGeneraCodiceFiscale = document.getElementById('btnGeneraCodiceFiscale');
    const codiceFiscaleContainer = document.getElementById('codiceFiscaleContainer');
    const codiceFiscaleElement = document.getElementById('codiceFiscale');

    btnGeneraCodiceFiscale.addEventListener('click', function () {
        // Recupera i dati necessari dal form 
        const formData = new FormData(document.getElementById('formRegister'));

        // Effettua una richiesta fetch per ottenere il codice fiscale
        fetch("/generate_codice_fiscale", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Mostra il codice fiscale nel container appropriato
            codiceFiscaleElement.textContent = data.codice_fiscale;
            codiceFiscaleContainer.style.display = 'block';
        })
        .catch(error => console.error("Errore nella richiesta: ", error));
    });
});