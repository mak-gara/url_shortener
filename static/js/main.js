$(document).ready(function () {

    // url shortener form
    $(this).on('submit', '#link-form', function (event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '',
            data: {
                long_link: $('#link').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
                if (data.short_link) {
                    // deleting
                    $('#link').removeClass('is-invalid');
                    $('.invalid-feedback').remove();
                    $('#long-link').remove();
                    // rendering
                    $('#link').val(data.short_link);
                    $('#link-form-description').before(`<a href="${data.long_link}" id="long-link" class="link-success">Long link</a>`);
                } else {
                    // deleting
                    $('#long-link').remove();
                    $('.invalid-feedback').remove();
                    // rendering
                    $('#link').addClass('is-invalid');
                    $('#link-label').after('<div class="invalid-feedback">Link is not valid</div>');
                }
            }
        });
    });
    // mail form
    $(this).on('submit', '#mailing-form', function (event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: 'mailing/subscribe/',
            data: {
                email: $('#email').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
                console.log(data);
                if (data.success) {
                    $('.invalid-feedback').remove();
                    $('#email').removeClass('is-invalid');

                    $('#email').addClass('is-valid').val('Thanks!');
                    $('#email-label').after('<div class="valid-feedback">You have successfully subscribed to the newsletter</div>');
                    $('.valid-feedback').delay(3000).fadeOut();

                    setTimeout(function () {
                        $('.valid-feedback').remove();
                        $('#email').removeClass('is-valid');
                    }, 3300);

                } else {
                    // deleting
                    $('.invalid-feedback').remove();
                    // rendering
                    $('#email').addClass('is-invalid');
                    $('#email-label').after('<div class="invalid-feedback">Error. Check the correctness of the specified data</div>');
                }
            }
        });
    });
});
