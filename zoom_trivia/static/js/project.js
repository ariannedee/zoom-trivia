$(document).ready(function () {
    $('a.button[disabled]').click(function (e) {
        e.preventDefault();
    });
});

function score(_this, answer_id, points) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.post({
        url: '/score',
        contentType: 'application/json',
        headers: {'X-CSRFToken': csrftoken},
        data: JSON.stringify({
            answer: answer_id,
            points: points
        }),
        success: (response) => {
            if (response === 'ok') {
                $(_this).siblings('button.points').removeClass('active');
                $(_this).addClass('active');
            }
        }
    });
}
