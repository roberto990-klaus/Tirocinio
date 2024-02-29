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



function downloadPDF(imageData, prediction) {
    // Effettua una richiesta AJAX al backend per generare il PDF
    $.ajax({
        url: '/generate_pdf',
        method: 'POST',
        data: JSON.stringify({ image_data: imageData, prediction: prediction }),
        contentType: 'application/json',
        xhrFields: {
            responseType: 'blob'  // Imposta il tipo di risposta come Blob
        },
        success: function(response) {
            // Converti la risposta in un URL temporaneo
            var url = window.URL.createObjectURL(response);

            // Crea un link per il download e simula il click
            var a = document.createElement('a');
            a.href = url;
            a.download = 'output.pdf';
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



document.addEventListener('DOMContentLoaded', function() {
    // Seleziona il menu di navigazione
    var navMenu = document.querySelector('.barra_navigazione');

    // Registra un listener per l'evento di scroll della finestra
    window.addEventListener('scroll', function() {
        // Calcola la posizione della finestra rispetto alla cima della pagina
        var scrollPosition = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;

        // Calcola la posizione a cui il menu dovrebbe scomparire, ad esempio 1/4 dell'altezza della finestra
        var hidePosition = window.innerHeight / 7;

        // Controlla se la posizione di scorrimento è oltre la posizione in cui il menu dovrebbe scomparire
        if (window.innerWidth <= 768 && scrollPosition > hidePosition) {
            // Nascondi il menu solo per schermi con larghezza inferiore o uguale a 768px
            navMenu.style.display = 'none';
        } else {
            // Altrimenti, mostra il menu settando la proprietà display a 'block'
            navMenu.style.display = 'block';
        }
    });

    // Registra un listener per l'evento di scroll della finestra
    window.addEventListener('scroll', function() {
        var languageContainer = document.getElementById('language-buttons-container');
        // Nascondi il contenitore dei pulsanti per la lingua solo per schermi con larghezza inferiore o uguale a 768px
        if (window.innerWidth <= 768 && window.scrollY > 100) {
            languageContainer.style.display = 'none';
        } else {
            // Altrimenti, mostra il contenitore dei pulsanti per la lingua
            languageContainer.style.display = 'block';
        }
    });
});







