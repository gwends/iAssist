const postBtn = $('#postBtn');
const currentBtn = $('#currentBtn');
const hiredBtn = $('#hiredBtn');
const historyBtn = $('#historyBtn');
const postForm = $('#postForm');
const currentForm = $('#currentForm');
const hiredForm = $('#hiredForm');
const historyForm = $('#historyForm');
const moymoy = $('#historyForm');

currentForm.css('display', 'none');
hiredForm.css('display', 'none');
historyForm.css('display', 'none');

postBtn.click(() => {
    console.log('success');
    postBtn.removeClass('btn-danger');
    currentBtn.removeClass('btn-danger');
    hiredBtn.removeClass('btn-danger');
    historyBtn.removeClass('btn-danger');
    postBtn.addClass('btn-danger');
    currentForm.css('display', 'none');
    hiredForm.css('display', 'none');
    historyForm.css('display', 'none');
    postForm.css('display', 'block');
});

currentBtn.click(() => {
    console.log('success');
    postBtn.removeClass('btn-danger');
    currentBtn.removeClass('btn-danger');
    hiredBtn.removeClass('btn-danger');
    historyBtn.removeClass('btn-danger');
    currentBtn.addClass('btn-danger');
    postForm.css('display', 'none');
    hiredForm.css('display', 'none');
    historyForm.css('display', 'none');
    currentForm.css('display', 'block');
});

hiredBtn.click(() => {
    console.log('success');
    postBtn.removeClass('btn-danger');
    currentBtn.removeClass('btn-danger');
    hiredBtn.removeClass('btn-danger');
    historyBtn.removeClass('btn-danger');
    hiredBtn.addClass('btn-danger');
    currentForm.css('display', 'none');
    postForm.css('display', 'none');
    historyForm.css('display', 'none');
    hiredForm.css('display', 'block');
});

historyBtn.click(() => {
    console.log('success');
    postBtn.removeClass('btn-danger');
    currentBtn.removeClass('btn-danger');
    hiredBtn.removeClass('btn-danger');
    historyBtn.removeClass('btn-danger');
    historyBtn.addClass('btn-danger');
    currentForm.css('display', 'none');
    hiredForm.css('display', 'none');
    postForm.css('display', 'none');
    historyForm.css('display', 'block');
});