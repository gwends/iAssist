const header = $('#header');
const employer = $('#employer');
const job_seeker = $('#job_seeker');
const employerForm = $('#employerForm');
const seekerForm = $('#seekerForm');

employerForm.css('display', 'none');

job_seeker.click(() => {
    header.html('Job Seeker');
    employer.removeClass('btn-primary');
    job_seeker.removeClass('btn-primary');
    job_seeker.addClass('btn-primary');
    employerForm.css('display', 'none');
    seekerForm.css('display', 'block');
});

employer.click(() => {
    header.html('Employer');
    employer.removeClass('btn-primary');
    job_seeker.removeClass('btn-primary');
    employer.addClass('btn-primary');
    seekerForm.css('display', 'none');
    employerForm.css('display', 'block');
});
