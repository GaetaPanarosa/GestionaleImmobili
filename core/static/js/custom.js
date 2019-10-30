$(document).ready(function () {
    $('#id_inizio_incarico').datetimepicker({
        timepicker:false,
        format:'Y-m-d',
        inline:true
    });
    $('#id_fine_incarico').datetimepicker({
        timepicker:false,
        format:'Y-m-d',
        inline:true
    });
    $('#id_scadenza').datetimepicker({
        timepicker:false,
        format:'Y-m-d',
        inline:true
    });
    console.log("entrato")
})