const sentBtn = $('#sentBtn');
const receiveBtn = $('#receiveBtn');
const sent = $('#sent');
const receive = $('#receive');

receive.css('display', 'none');

sentBtn.click(() => {
    receiveBtn.removeClass('btn-danger');
    sentBtn.addClass('btn-danger');
    receive.css('display', 'none');
    sent.css('display', 'block');
});

receiveBtn.click(() => {
    sentBtn.removeClass('btn-danger');
    receiveBtn.addClass('btn-danger');
    sent.css('display', 'none');
    receive.css('display', 'block');
});