$(document).ready(function () {
    let getCurrentTimer;
    let countdownTimer;

    const timer = $('div.timer');
    function update_time_left() {
        $.get({
            url: url,
            success: (response) => {
                if (response !== 'None') {
                    console.log(`Get current time ${response}`);
                    timer.removeAttr('hidden');
                    if (response === '0') {
                        timer.text("Time's up!");
                        clearInterval(countdownTimer);
                    } else {
                        timer.text(response);
                        clearInterval(countdownTimer);
                        countdownTimer = window.setInterval(countDown, 1000);
                    }
                }
            }
        });
    }

    function countDown() {
        const secondsLeft = Number(timer.text());
        console.log(secondsLeft);
        const nextValue = Math.max(secondsLeft - 1, 0);
        if (nextValue === 0) {
            clearInterval(countdownTimer);
            timer.text("Time's up!");
        } else {
            timer.text(nextValue);
        }
    }

    getCurrentTimer = window.setInterval(update_time_left, 10000);
    if (timer.attr('hidden')) {
        update_time_left();
    } else {
        countdownTimer = window.setInterval(countDown, 1000);
    }
});
