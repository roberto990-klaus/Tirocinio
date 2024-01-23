 // JavaScript per gestire il passaggio tra il form di login e quello di registrazione
 const formLogin = document.getElementById('formLogin');
 const formRegister = document.getElementById('formRegister');
 const formRecuperoPassword = document.getElementById('formRecuperoPassword');
 const linkRegistrazione = document.getElementById('linkRegistrazione');
 const linkAccedi = document.getElementById('linkAccedi');
 const linkAccedi2 = document.getElementById('linkAccedi2');
 const linkPasswordDimenticata = document.getElementById('linkPasswordDimenticata');
 
 // Inizialmente nascondiamo il form di registrazione
 formRegister.style.display = 'none';


 // Aggiungiamo un event listener al link "Passa a registrazione"
 linkRegistrazione.addEventListener('click', (e) => {
     e.preventDefault(); 
     formLogin.style.display = 'none';
     formRegister.style.display = 'block';
     formRecuperoPassword.style.display = 'none';
     hideAlerts(); // Nascondi gli alert quando si cambia form
 });

 linkAccedi.addEventListener('click', (e) => {
     e.preventDefault();
     formRegister.style.display = 'none';
     formLogin.style.display = 'block';
     formRecuperoPassword.style.display = 'none';
     hideAlerts(); // Nascondi gli alert quando si cambia form
 });


 linkAccedi2.addEventListener('click', (e) => {
     e.preventDefault();
     formRegister.style.display = 'none';
     formLogin.style.display = 'block';
     formRecuperoPassword.style.display = 'none';
     hideAlerts(); // Nascondi gli alert quando si cambia form
 });

 linkPasswordDimenticata.addEventListener('click', (e) => {
     e.preventDefault();
     formLogin.style.display = 'none';
     formRegister.style.display = 'none';
     formRecuperoPassword.style.display = 'block'; // Mostra il form di recupero password
     hideAlerts();
 });

 // Funzione per nascondere gli alert
 function hideAlerts() {
     const successAlert = document.getElementById('success-alert');
     const errorAlert = document.getElementById('error-alert');
     const errorAlertLogin = document.getElementById('error-alert-login');
     if (successAlert) {
         successAlert.style.display = 'none';
     }
     if (errorAlert) {
         errorAlert.style.display = 'none';
     }
     if (errorAlertLogin) {
         errorAlertLogin.style.display = 'none';
     }
 }