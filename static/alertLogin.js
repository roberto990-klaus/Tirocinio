//Script per l'alert nel form di login
document.addEventListener('DOMContentLoaded', function () {
    const formLogin = document.getElementById('formLogin');
    const errorAlertLogin = document.getElementById('error-alert-login');
    const errorMessageLogin = document.getElementById('error-message-login');

    formLogin.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(formLogin);

        fetch("/login", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                errorMessageLogin.textContent = data.error;
                errorAlertLogin.style.display = "block";
            } else if (data.redirect) {
                window.location.href = data.redirect;
            }
        })
        .catch(error => console.error("Errore nella richiesta: ", error));
    });
});

//Script per l'alert nel form di recupero password
document.addEventListener('DOMContentLoaded', function () {
    const formRecuperoPassword = document.getElementById('formRecuperoPassword');
    const successAlertRecupero = document.getElementById('success-alert-recupero');
    const errorAlertRecupero = document.getElementById('error-alert-recupero');
    const successMessageRecupero = document.getElementById('success-message-recupero');
    const errorMessageRecupero = document.getElementById('error-message-recupero');

    formRecuperoPassword.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(formRecuperoPassword);

        fetch("/recupera_password", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                successMessageRecupero.textContent = data.success;
                successAlertRecupero.style.display = "block";
                errorAlertRecupero.style.display = "none";
            } else if (data.error) {
                errorMessageRecupero.textContent = data.error;
                errorAlertRecupero.style.display = "block";
                successAlertRecupero.style.display = "none";
            }
        })
        .catch(error => console.error("Errore nella richiesta: ", error));
    });
});
