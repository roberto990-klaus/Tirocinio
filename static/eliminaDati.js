document.addEventListener('DOMContentLoaded', function () {
    const formEliminazione = document.getElementById('formEliminazione');
    const errorAlert = document.getElementById('error-alert');
    const errorMessage = document.getElementById('error-message');
    const successAlert = document.getElementById('success-alert');
    const successMessage = document.getElementById('success-message');
    const btnElimina = document.getElementById('btnElimina');

    formEliminazione.addEventListener('submit', function (e) {
        e.preventDefault();

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
            } else if (data.success) {
                successMessage.textContent = data.success;
                successAlert.style.display = "block";
                errorAlert.style.display = "none";

                // reindirizzamento alla pagina di login dopo l'eliminazione del profilo
                setTimeout(function() {
                    window.location.href = "/login.html";
                }, 3000);
            }
        })
        .catch(error => console.error("Errore nella richiesta: ", error));
    });

    btnElimina.addEventListener('click', function () {
        errorAlert.style.display = 'none';
    });
});