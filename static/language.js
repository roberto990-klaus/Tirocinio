$(document).ready(function() {
    var lang = 'en'; // Imposta l'inglese come lingua predefinita

    // Funzione per caricare le traduzioni
    function loadTranslations(lang) {
        $.getJSON('../translation/' + lang + '.json', function(data) {
            // Form di login
            $('#titolo_pagina').text(data['titolo_pagina']);
            $('#email_login').attr('placeholder', data['email_login_placeholder']);
            $('#password_login').attr('placeholder', data['password_login_placeholder']);
            $('#ricorda_password').text(data['ricorda_password']);
            $('#linkPasswordDimenticata').text(data['linkPasswordDimenticata']);
            $('#btnLogin_label').text(data['btnLogin_label']);
            $('#registrazione_text').text(data['registrazione_text']);
            $('#registrazione_link').text(data['registrazione_link']);
            $('#error-message-login').text(data['error-message-login']);

            // Form recupera password
            $('#recupera_password').text(data['recupera_password']);
            $('#email_recupero_password').attr('placeholder', data['email_recupero_password_placeholder']);
            $('#btnrecupera_password').text(data['btnrecupera_password']);
            $('#torna_login').text(data['torna_login']);
            $('#success-message-recupero').text(data['success_message_recupero']);
            $('#error-message-recupero').text(data['error_message_recupero']);

            // Form di registrazione
            $('#titolo_pagina2').text(data['titolo_pagina2']);
            $('#titolo_nome').text(data['titolo_nome']);
            $('#nome').attr('placeholder', data['nome_placeholder']);
            $('#titolo_cognome').text(data['titolo_cognome']);
            $('#cognome').attr('placeholder', data['cognome_placeholder']);
            $('#sesso').text(data['sesso']);
            $('#maschio_label').text(data['maschio_label']);
            $('#donna_label').text(data['donna_label']);
            $('#luogo_nascita').text(data['luogo_nascita']);
            $('#luogo_di_nascita').attr('placeholder', data['luogo_di_nascita_placeholder']);
            $('#data_di_nascita').text(data['data_di_nascita']);
            $('#data').attr('placeholder', data['data_placeholder']);
            $('#cod_fiscale').text(data['cod_fiscale']);
            $('#email').attr('placeholder', data['email_placeholder']);
            $('#password').attr('placeholder', data['password_placeholder']);
            $('#button_reg').text(data['button_reg']);
            $('#account_esistente').text(data['account_esistente']);
            $('#ritorna_login').text(data['ritorna_login']);
            $('#seleziona_lingua').text(data['seleziona_lingua']);
            $('#success-alert').text(data['success-alert']);
            $('#error-alert').text(data['error-alert']);

            //Pagina after_login
            $('#nav_visualizza').text(data['nav_visualizza']);
            $('#nav_modifica').text(data['nav_modifica']);
            $('#nav_info').text(data['nav_info']);
            $('#nav_canc').text(data['nav_canc']);
            $('#nav_esci').text(data['nav_esci']);
            $('#carica_immagine').text(data['carica_immagine']);
            $('#success-alert-carica').text(data['success-alert-carica']);

            
            //Form visualizza analisi
            $('#titolo_visualizza').text(data['titolo_visualizza']);
            $('#1colonna').text(data['1colonna']);
            $('#2colonna').text(data['2colonna']);
            $('#3colonna').text(data['3colonna']);
            $('#4colonna').text(data['4colonna']);





            //Form modifica dati
            $('#titolo_modifica').text(data['titolo_modifica']);
            $('#inserisci_email').text(data['inserisci_email']);
            $('#inserisci_password').text(data['inserisci_password']);
            $('#nuovo_nome').attr('placeholder', data['nuovo_nome_placeholder']);
            $('#nuovo_cognome').attr('placeholder', data['nuovo_cognome_placeholder']);
            $('#nuova_data').attr('placeholder', data['nuova_data_placeholder']);
            $('#nuovo_codice_fiscale').attr('placeholder', data['nuovo_codice_fiscale_placeholder']);
            $('#nuova_password').attr('placeholder', data['nuova_password_placeholder']);
            $('#salva_modifiche').text(data['salva_modifiche']);
            $('#titolo_nuovo_nome').text(data['titolo_nuovo_nome']);
            $('#titolo_nuovo_cognome').text(data['titolo_nuovo_cognome']);
            $('#titolo_nuova_data').text(data['titolo_nuova_data']);
            $('#titolo_nuovo_cf').text(data['titolo_nuovo_cf']);
            $('#titolo_nuova_password').text(data['titolo_nuova_password']);
            $('#salva_modifiche').text(data['salva_modifiche']);
            $('#success-message-modifica').text(data['success-message-modifica']);
            $('#error-message-modifica').text(data['error-message-modifica']);


            //Form informazioni progetto
            $('#titolo_info').text(data['titolo_info']);




            //Form elimina profilo
            $('#titolo_elimina').text(data['titolo_elimina']);
            $('#titolo_elimina_dati').text(data['titolo_elimina_dati'])
            $('#btnElimina').text(data['btnElimina']);
            $('#success-message-elimina').text(data['success-message-elimina']);
            $('#error-message-elimina').text(data['error-message-elimina']);


        });
    }

    // Carica le traduzioni iniziali
    loadTranslations(lang);

    // Funzione per salvare la lingua selezionata nello storage locale
    function saveLanguagePreference(lang) {
        localStorage.setItem('selectedLang', lang);
    }

    // Funzione per aprire e chiudere il menu a tendina
    function toggleDropdown() {
        var dropdownContent = $('#languageDropdown');
        dropdownContent.toggle(); // Inverti lo stato di visualizzazione del menu a tendina
    }

    // Gestisci l'evento mouseenter sul pulsante per aprire il menu a tendina al passaggio del mouse
    $('.dropbtn').mouseenter(function() {
        toggleDropdown();
    });

    // Gestisci l'evento mouseleave del menu a tendina per chiudere il menu quando il mouse esce dall'area del menu
    $('#language-buttons-container').mouseleave(function() {
        var dropdownContent = $('#languageDropdown');
        dropdownContent.hide(); // Nascondi il menu a tendina
    });

    // Gestisci il click sui pulsanti del menu a tendina
    $('.dropdown-content button').click(function() {
        var selectedLang = $(this).data('lang');
        lang = selectedLang;
        loadTranslations(lang);
        saveLanguagePreference(lang); // Salva la lingua selezionata nello storage locale
        toggleDropdown(); // Chiudi il menu a tendina dopo aver selezionato una lingua
    });
});
