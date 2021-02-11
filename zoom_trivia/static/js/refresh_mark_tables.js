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

reload_marking_tables();
window.setInterval(reload_marking_tables, 3000);
