$(document).ready(function() {
    var lang = 'en'; // Imposta l'inglese come lingua predefinita
    var data;

    // Funzione per caricare le traduzioni
    function loadTranslations(lang) {
        $.getJSON('../translation/' + lang + '.json', function(responseData) {
            data = responseData;
            // Form di login
            $('#titolo_pagina').text(data['titolo_pagina']);
            $('#email_login').attr('placeholder', data['email_login_placeholder']);
            $('#password_login').attr('placeholder', data['password_login_placeholder']);
            $('#ricorda_password').text(data['ricorda_password']);
            $('#linkPasswordDimenticata').text(data['linkPasswordDimenticata']);
            $('#btnLogin_label').text(data['btnLogin_label']);
            $('#registrazione_text').text(data['registrazione_text']);
            $('#registrazione_link').text(data['registrazione_link']);
            $('#error-alert-login').text(data['error-alert-login']);

            // Form recupera password
            $('#recupera_password').text(data['recupera_password']);
            $('#email_recupero_password').attr('placeholder', data['email_recupero_password_placeholder']);
            $('#btnrecupera_password').text(data['btnrecupera_password']);
            $('#torna_login').text(data['torna_login']);
            $('#success-alert-recupero').text(data['success-alert-recupero']);
            $('#error-alert-recupero').text(data['error-alert-recupero']);

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
            $('#data_nascita').text(data['data_nascita']);
            $('#data').attr('placeholder', data['data_placeholder']);
            $('#cod_fiscale').text(data['cod_fiscale']);
            $('#error-generazione-cf').text(data['error-generazione-cf']);
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
            $('#error-alert-invalid-format').text(data['error-alert-invalid-format']);
            $('#error-alert-carica').text(data['error-alert-carica']);
            $('#success-alert-carica').text(data['success-alert-carica']);


            
            //Form visualizza analisi
            $('#titolo_visualizza').text(data['titolo_visualizza']);
            $('#1colonna').text(data['1colonna']);
            $('#2colonna').text(data['2colonna']);
            $('#3colonna').text(data['3colonna']);
            $('#4colonna').text(data['4colonna']);





            //Form modifica dati
            $('#titolo_info_utente').text(data['titolo_info_utente']);
            $('#titolo_modifica').text(data['titolo_modifica']);
            $('#nome_attuale').text(data['nome_attuale']);
            $('#cognome_attuale').text(data['cognome_attuale']);
            $('#data_nascita_attuale').text(data['data_nascita_attuale']);
            $('#codice_fiscale_attuale').text(data['codice_fiscale_attuale']);
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
            $('#success-alert-modifica').text(data['success-alert-modifica']);
            $('#error-alert-modifica').text(data['error-alert-modifica']);


            //Form informazioni progetto
            $('#titolo_info').text(data['titolo_info']);




            //Form elimina profilo
            $('#titolo_elimina').text(data['titolo_elimina']);
            $('#titolo_elimina_dati').text(data['titolo_elimina_dati'])
            $('#btnElimina').text(data['btnElimina']);
            $('#success-alert-elimina').text(data['success-alert-elimina']);
            $('#error-alert-elimina').text(data['error-alert-elimina']);
            $('#seleziona_lingua_mobile').text(data['seleziona_lingua_mobile']);

            // Aggiorna il testo del menu burger
            updateMobileMenuText(data);
        });
    }

    // Funzione per aggiornare il testo del menu burger
    function updateMobileMenuText(data) {
        $('#nav_visualizza_mobile').text(data['nav_visualizza_mobile']);
        $('#nav_modifica_mobile').text(data['nav_modifica_mobile']);
        $('#nav_info_mobile').text(data['nav_info_mobile']);
        $('#nav_canc_mobile').text(data['nav_canc_mobile']);
        // Aggiungi altre istruzioni per gli altri link del menu burger qui
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

    // Funzione per aprire e chiudere il menu a tendina per la selezione della lingua su dispositivi mobili
    function toggleDropdownMobile() {
        var dropdownMobileContent = $('#languageDropdownMobile');
        dropdownMobileContent.toggle(); // Inverti lo stato di visualizzazione del menu a tendina
    }


    // Gestisci l'evento mouseenter sul pulsante per aprire il menu a tendina al passaggio del mouse
    $('.dropbtn').mouseenter(function() {
        toggleDropdown();
        toggleDropdownMobile();
    });

    // Gestisci l'evento mouseleave del menu a tendina per chiudere il menu quando il mouse esce dall'area del menu
    $('#language-buttons-container').mouseleave(function() {
        var dropdownContent = $('#languageDropdown');
        dropdownContent.hide(); // Nascondi il menu a tendina
    });

    // Gestisci l'evento mouseleave del menu a tendina per chiudere il menu quando il mouse esce dall'area del menu
    $('#language-buttons-mobile').mouseleave(function() {
        var dropdownMobileContent = $('#languageDropdownMobile');
        dropdownMobileContent.hide(); // Nascondi il menu a tendina
    });

    // Gestisci il click sui pulsanti del menu a tendina
    $('.dropdown-content button').click(function() {
        var selectedLang = $(this).data('lang');
        lang = selectedLang;
        loadTranslations(lang);
        saveLanguagePreference(lang); // Salva la lingua selezionata nello storage locale
        toggleDropdown(); // Chiudi il menu a tendina dopo aver selezionato una lingua
        toggleDropdownMobile(); // Chiudi il menu a tendina dopo aver selezionato una lingua
    });
});


