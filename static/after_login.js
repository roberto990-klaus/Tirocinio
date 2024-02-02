 src="https://code.jquery.com/jquery-3.6.4.min.js"


  $(document).ready(function() {
    $('form').submit(function(event) {
      event.preventDefault();

      var formData = new FormData($(this)[0]);

      $.ajax({
        url: '/predict',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function(response) {
          $('#prediction_result').text('Risultato della previsione: ' + response.prediction);
        },
        error: function(error) {
          console.log(error);
          $('#prediction_result').text('Errore nella previsione.');
        }
      });
    });
  });