$(document).ready(function() {
    var lang = 'it'; // Lingua predefinita da visualizzare

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

            // Form recupera password
            $('#recupera_password').text(data['recupera_password']);
            $('#email_recupero_password').attr('placeholder', data['email_recupero_password_placeholder']);
            $('#btnrecupera_password').text(data['btnrecupera_password']);
            $('#torna_login').text(data['torna_login']);

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
        });
    }

    // Carica le traduzioni iniziali
    loadTranslations(lang);

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
        toggleDropdown(); // Chiudi il menu a tendina dopo aver selezionato una lingua
    });
});
