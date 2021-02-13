$(document).ready(function () {
    $('a.button').click(function (e) {
        if (this.hasAttribute('disabled')) {
            e.preventDefault();
            return false;
        }
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

function getRequest(url) {
    $.get({
        url: url,
        success: (response) => {
            console.log(`GET ${url}: ${response}`);
        }
    });
}
