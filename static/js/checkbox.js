$('.form-correct-input').click(function(ev) {
    ev.preventDefault();
    var $this = $(this),
        aid = $this.data('aid');
    $.ajax('/correct/', {
        method: 'POST',
        data: {
            aid: aid
        }
    }).done(function(data) {
        console.log(data['error']);
        if (data['error'] == "") {
            if (data['value']) {
                $('.correct-' + aid).prop('correct', true);
            } else {
                $('.correct-' + aid).prop('correct', false);
            }
        } else {
            alert('Action not permitted')
        }
    });
});