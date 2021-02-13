$(document).ready(function () {
    function reload_marking_tables() {
        $('table').each((index, table) => {
            var url = table.id;
            $.get({
                url: url,
                success: (response) => {
                    $(table).html(response);
                }
            });
        });
    }

    window.setInterval(reload_marking_tables, 10000);
});
