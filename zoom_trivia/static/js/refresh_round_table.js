$(document).ready(function () {
    function reload_round_table() {
        $.get({
            url: '/1/game_table/',
            success: (response) => {
                $('table.player').html(response);
            }
        });
    }

    if ($('table.player')) {
        window.setInterval(reload_round_table, 3000);
    }
});
