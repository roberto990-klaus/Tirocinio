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
                window.location.href = "/login";
            }, 4000);
        })
        .catch(error => console.error("Errore nella richiesta: ", error));
    });
});


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
