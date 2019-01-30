$(document).ready(function(){
    $('#clear').click(function() {
        $('#template').val('');
        $('#render').val('');
        $('#values').val('');
        $('#sql_template_name').val('');
        $('#render').html('');
    });


    $('#save').click(function() {
        $.post('/save', {
            template: $('#template').val(),
            values: $('#values').val(),
            sql_template_name: $('#sql_template_name').val()
        }).done(function(response) {
            // Display the answer
            $('#render').html("template saved");
            window.location.replace("/load/" + $('#sql_template_name').val())
        });
    });


    $('#convert').click(function() {
        var is_checked_showwhitespaces = $('input[name="showwhitespaces"]').is(':checked') ? 1:0;
        var is_checked_dummyvalues = $('input[name="dummyvalues"]').is(':checked') ? 1:0;
        var input_type = $('input[name="input_type"]:checked').val();


        // Push the input to the Jinja2 api (Python)
        $.post('/convert', {
            template: $('#template').val(),
            values: $('#values').val(),
            input_type: input_type,
            showwhitespaces: is_checked_showwhitespaces,
            dummyvalues: is_checked_dummyvalues
        }).done(function(response) {
            // HTMLize the answer: Grey out the white spaces chars if any
            //response = response.replace(/ /g, '&nbsp;');
            //response = response.replace(/\n/g, '<br />');
            //response = response.replace(/•/g, '<span class="whitespace">•</span>');

            // Display the answer
            $('#render').val(response);
        });
    });
});
