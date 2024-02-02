//Script per gli alert nel form di registrazione
document.addEventListener('DOMContentLoaded', function () {
    const formRegister = document.getElementById('formRegister');
    const errorAlert = document.getElementById('error-alert');
    const errorMessage = document.getElementById('error-message');
    const successAlert = document.getElementById('success-alert');
    const successMessage = document.getElementById('success-message');
    const btnRegistrazione = document.getElementById('btnRegistrazione');

    formRegister.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(formRegister);

        fetch("/register", {
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

    btnRegistrazione.addEventListener('click', function () {
        errorAlert.style.display = 'none';
    });
});