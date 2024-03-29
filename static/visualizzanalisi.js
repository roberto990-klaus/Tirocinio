$(document).ready(function () {
    var table = $('#imageTable').DataTable({
        "order": [[1, "desc"]], // Ordina per la seconda colonna (indice 1) in ordine discendente (desc)
        "initComplete": function () {
            this.api().columns().every(function () {
                var column = this;
                if (column.index() === 1) { // Se si tratta della colonna delle date
                    var title = $(this.header()).text();
                    $(this.header()).html(title + ' <span class="sort-icon"></span>');
                }
            });
        }
    });

    $('#imageTable').on('click', '#2colonna', function () {
        var column = table.column($(this));
        var icon = $(this).find('.sort-icon');

        // Rimuovi tutte le frecce
        $('.sort-icon').html('');

        // Aggiungi la freccia corretta alla colonna cliccata
        if (column.order()[0] === 'asc') {
            icon.html('&#9650;');
        } else {
            icon.html('&#9660;');
        }
    });
});

function openModal(imageData) {
    var modal = document.getElementById("imageModal");
    var modalImg = document.getElementById("modalImage");
    modal.style.display = "block";
    modalImg.src = "data:image/jpeg;base64," + imageData;
}

function closeModal() {
    var modal = document.getElementById("imageModal");
    modal.style.display = "none";
}


// Funzione per generare un nome casuale di 10 caratteri alfanumerici
function generateRandomName() {
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var randomName = '';
    for (var i = 0; i < 10; i++) {
        randomName += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return randomName;
}


function downloadPDF(imageData, prediction) {
    // Cattura il valore della lingua selezionata
    var lang = $('#languageDropdown').find('.active').data('lang');
    console.log('Lingua selezionata:', lang); // Debug: stampa la lingua selezionata nella console

    // Effettua una richiesta AJAX al backend per generare il PDF
    $.ajax({
        url: '/generate_pdf?lingua=' + lang,
        method: 'POST',
        data: JSON.stringify({ image_data: imageData, prediction: prediction }),
        contentType: 'application/json',
        xhrFields: {
            responseType: 'blob'  // Imposta il tipo di risposta come Blob
        },
        success: function(response) {
            console.log('Risposta del server:', response); // Debug: stampa la risposta del server nella console
            // Converti la risposta in un URL temporaneo
            var url = window.URL.createObjectURL(response);

            // Genera un nome casuale per il PDF
            var pdfName = generateRandomName() + '.pdf';

            // Crea un link per il download e simula il click
            var a = document.createElement('a');
            a.href = url;
            a.download = pdfName;  // Utilizza il nome casuale del PDF
            document.body.appendChild(a);
            a.click();

            // Rilascia la risorsa URL
            window.URL.revokeObjectURL(url);
        },
        error: function(xhr, status, error) {
            // Gestisci eventuali errori
            console.error('Errore durante il download del PDF:', error);
        }
    });
}



// Funzione per selezionare la lingua
function selectLanguage(lang) {
    // Rimuovi la classe 'active' da tutti i pulsanti della lingua
    $('#languageDropdown button').removeClass('active');
    // Aggiungi la classe 'active' al pulsante della lingua selezionata
    $('#languageDropdown button[data-lang="' + lang + '"]').addClass('active');
}


function eliminaImmagine(id) {
    // Conferma con l'utente se desidera eliminare l'immagine
    if (confirm("Sei sicuro di voler eliminare questa immagine?")) {
        // Effettua una richiesta AJAX per eliminare l'immagine dal database
        $.ajax({
            url: '/elimina_immagine',
            method: 'POST',
            data: { immagine_id: id },
            success: function(response) {
                // Se l'eliminazione è riuscita, ricarica la pagina per aggiornare la tabella delle immagini
                location.reload();
            },
            error: function(xhr, status, error) {
                // Gestisci eventuali errori
                console.error('Errore durante l\'eliminazione dell\'immagine:', error);
            }
        });
    }
}



// Apri il modale di conferma eliminazione
function openDeleteModal(button) {
    // Recupera l'ID dell'immagine dall'attributo data
    var id = button.getAttribute('data-image-id');
    var modal = document.getElementById("deleteModal");
    modal.style.display = "block";
    
    // Imposta l'ID dell'immagine nel modale per l'eliminazione
    document.getElementById("delete-image-id").value = id;
}

// Funzione chiamata quando viene confermata l'eliminazione
function deleteConfirmed(event) {
    event.preventDefault(); // Impedisci il comportamento predefinito dell'evento di clic

    var id = document.getElementById("delete-image-id").value;
    // Effettua l'eliminazione dell'immagine
    eliminaImmagine(id); // Chiamata alla funzione per l'eliminazione effettiva
    closeDeleteModal(); // Chiude il modale di conferma eliminazione
}



// Chiudi il modale di conferma eliminazione
function closeDeleteModal(event) {
    var modal = document.getElementById("deleteModal");
    modal.style.display = "none";
    event.preventDefault(); // Impedisci il comportamento predefinito dell'evento di clic
}



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