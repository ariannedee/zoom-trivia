$(document).ready(function () {
    let getCurrentTimer;
    let countdownTimer;

    const timer = $('div.timer');
    const secondsLeftDiv = $('div#seconds-left');
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
                        secondsLeftDiv.text(0);
                    } else {
                        secondsLeftDiv.text(response);
                        countDown();
                        clearInterval(countdownTimer);
                        countdownTimer = window.setInterval(countDown, 1000);
                    }
                }
            }
        });
    }

    function countDown() {
        const secondsLeft = Number(secondsLeftDiv.text());
        console.log(secondsLeft);
        const nextValue = Math.max(secondsLeft - 1, 0);
        if (nextValue === 0) {
            clearInterval(countdownTimer);
            timer.text("Time's up!");
            secondsLeftDiv.text(0);
        } else {
            let text = '';
            if (nextValue > 60) {
                text += `${Math.floor(nextValue/60)}m `
            }
            text += `${Math.floor(nextValue % 60)}s `
            timer.text(text);
            secondsLeftDiv.text(nextValue);
        }
    }

    getCurrentTimer = window.setInterval(update_time_left, 10000);
    if (timer.attr('hidden')) {
        update_time_left();
    } else {
        countdownTimer = window.setInterval(countDown, 1000);
    }
});
