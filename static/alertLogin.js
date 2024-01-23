//Script per l'alert nel form di login
document.addEventListener('DOMContentLoaded', function () {
    const formLogin = document.getElementById('formLogin');
    const errorAlertLogin = document.getElementById('error-alert-login');
    const errorMessageLogin = document.getElementById('error-message-login');
    const btnLogin = document.getElementById('btnLogin');


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

    btnLogin.addEventListener('click', function () {
        errorAlertLogin.style.display = 'none';
    });
});