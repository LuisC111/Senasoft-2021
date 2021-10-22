$("#pro-form input").keyup(function() {

    var numValid = 0;
    $("#pro-form input[required]").each(function() {
        if (this.validity.valid) {
            numValid++;
        }
    });

    var progress = $("#progress"),
        progressMessage = $("#progress-message");

    if (numValid == 0) {
        progress.attr("value", "0");
        progressMessage.text("Completa el formulario.");
    }
    if (numValid == 1) {
        progress.attr("value", "14.285");
        progressMessage.text("Continúa!.");
    }
    if (numValid == 2) {
        progress.attr("value", "28.571");
        progressMessage.text("Sigue así!");
    }
    if (numValid == 3) {
        progress.attr("value", "42.857");
        progressMessage.text("Falta poco.");
    }
    if (numValid == 4) {
        progress.attr("value", "57.142");
        progressMessage.text("Ya casi está listo!");
    }
    if (numValid == 5) {
        progress.attr("value", "100");
        progressMessage.text("Listo.");
    }

});