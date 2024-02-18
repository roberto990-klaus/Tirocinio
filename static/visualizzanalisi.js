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

    $('#imageTable').on('click', 'th', function () {
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