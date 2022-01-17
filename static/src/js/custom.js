//var rowUpdate = 0

// All Default Breadcrumb hide
$(".job_default_breadcrumb_remove").find(".breadcrumb").hide();
// Loader function
$(function () {
    $(".preload").fadeOut(function () {
        $(".content").fadeIn();
    });
});

$(".toggle-password").click(function () {

    $(this).toggleClass("fa-eye fa-eye-slash");
    var input = $($(this).attr("toggle"));
    if (input.attr("type") == "password") {
        input.attr("type", "text");
    } else {
        input.attr("type", "password");
    }

});


$("#extension_button").click(function () {

    var base_url = window.location.origin;
    var data_job_create = "?name=" + $("input[name='partner_name']").val() + "&partner_name=" + $("input[name='partner_name']").val() + "&email_from=" + $("input[name='email_from']").val() + "&partner_mobile=" + $("input[name='partner_mobile']").val() + "&salary_expected=" + $("input[name='salary_expected']").val() + "&father=" + $("input[name='father']").val() + "&mother=" + $("input[name='mother']").val() + "&gender=" + $("select[name='gender']").val() + "&birthday=" + $("input[name='birthday']").val() + "&national_id=" + $("input[name='national_id']").val() + "&job_id=" + $("input[name='job_id']").val() + "&department_id=" + $("input[name='department_id']").val() ;
    const url_job_create = base_url + '/create/user/job' + data_job_create;

    var xhttp_job_create = new XMLHttpRequest();

    xhttp_job_create.open("GET", url_job_create, true);
    xhttp_job_create.send();

    // var data_pay = "?job_id=" + $("input[name='job_id']").val() + "&transaction_no=" + $("input[name='transaction_no']").val() + "&transaction_date=" + $("input[name='transaction_date']").val() + "&job_applicant_id=" + $("input[name='job_applicant_id']").val();
    // const url_pay = base_url + '/create/user/payorder/' + data_pay;
    //
    // var xhttp_pay = new XMLHttpRequest();
    //
    // xhttp_pay.open("GET", url_pay, true);
    // xhttp_pay.send();

});

$("#applicant_submit").click(function () {

    var base_url = window.location.origin;
    var data = "?name=" + $("input[name='partner_name']").val() + "&login=" + $("input[name='email_from']").val() + "&password=" + $("input[name='password']").val();
    const url = base_url + '/create/user' + data;


    var xhttp = new XMLHttpRequest();

    xhttp.open("GET", url, true);
    xhttp.send();

    var data_job = "?name=" + $("input[name='partner_name']").val() + "&partner_name=" + $("input[name='partner_name']").val() + "&email_from=" + $("input[name='email_from']").val() + "&partner_mobile=" + $("input[name='partner_mobile']").val() + "&password=" + $("input[name='password']").val() + "&confirm_password=" + $("input[name='confirm_password']").val();

    const url_job = base_url + '/create/user/job/applicant' + data_job;
    var xhttp_job = new XMLHttpRequest();

    xhttp_job.open("GET", url_job, true);
    xhttp_job.send();

});

$("#position_button").click(function () {

    var base_url = window.location.origin;
    var data_job_create = "?partner_name=" + $("input[name='partner_name']").val() + "&email_from=" + $("input[name='email_from']").val() + "&partner_mobile=" + $("input[name='partner_mobile']").val() + "&salary_expected=" + $("input[name='salary_expected']").val() + "&father=" + $("input[name='father']").val() + "&mother=" + $("input[name='mother']").val() + "&gender=" + $("select[name='gender']").val() + "&birthday=" + $("input[name='birthday']").val() + "&national_id=" + $("input[name='national_id']").val() + "&job_id=" + $("input[name='job_id']").val() + "&department_id=" + $("input[name='department_id']").val() + "&transaction_no=" + $("input[name='transaction_no']").val()+ "&transaction_date=" + $("input[name='transaction_date']").val()+ "&description=" + $("input[name='description']").val()+ "&job_applicant_id=" + $("input[name='job_applicant_id']").val();
    const url_job_create = base_url + '/hr-applicant/' + data_job_create;

    var xhttp_job = new XMLHttpRequest();

    xhttp_job.open("GET", url_job_create, true);
    xhttp_job.send();

});

// $('#psw, #confirm_psw').on('keyup', function () {
//     var psw = document.getElementById("psw")
//         , confirm_psw = document.getElementById("confirm_psw");
//
//     function validatePassword() {
//         if (psw.value != confirm_psw.value) {
//             confirm_psw.setCustomValidity("Passwords Don't Match");
//         } else {
//             confirm_psw.setCustomValidity('');
//         }
//     }
//
//     psw.onchange = validatePassword;
//     confirm_psw.onkeyup = validatePassword;
//
// });

function calculate_age_birth(birthday, show_field_name) {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1; //As January is 0.
    var yyyy = today.getFullYear();

    if (birthday > today) {
        $(show_field_name).val("0")
    } else {
        $(show_field_name).val(yyyy - birthday.split("/")[2] - ((mm, dd) < (birthday.split("/")[1], birthday.split("/")[0])))
    }
}

function change_applicant_birthday() {
    var birthday = $("input[id=birthday]").val();
    if (isValidDate(birthday) == false) {
        calculate_age_birth(birthday, "input[id=birthday]");
    }
}

$("#verify_submit").click(function () {
    $("#verify_submit").hide();
    $("#show").show();
    var base_url = window.location.origin;

    var data_job_ref = "?xxx=" + $("input[id='xxx']").val();
    console.log($("input[id='xxx']").val())
    const url_job_ref = base_url + '/verified' + data_job_ref;

    var xhttp_job_ref = new XMLHttpRequest();

    xhttp_job_ref.open("GET", url_job_ref, true);
    xhttp_job_ref.send();
});

$("#admit_card_download").click(function () {

    var base_url = window.location.origin;

    var data_job_admit = "?xx=" + $("input[id='xx']").val();
    console.log($("input[id='xx']").val());
    const url_job_ref = base_url + '/admit-card' + data_job_admit;

    var xhttp_job_ref = new XMLHttpRequest();

    xhttp_job_ref.open("GET", url_job_ref, true);
    xhttp_job_ref.send();
});


// $('#psw').on('keyup', function () {
//
//     var psw = document.getElementById("psw");
//     var letter = document.getElementById("letter");
//     var capital = document.getElementById("capital");
//     var number = document.getElementById("number");
//     var length = document.getElementById("length");
//
// // When the user clicks on the password field, show the message box
//     psw.onfocus = function () {
//         document.getElementById("message_id").style.display = "block";
//     }
//
// // When the user clicks outside of the password field, hide the message box
//     psw.onblur = function () {
//         document.getElementById("message_id").style.display = "none";
//     }
//
// // When the user starts to type something inside the password field
//     psw.onkeyup = function () {
//         // Validate lowercase letters
//         var lowerCaseLetters = /[a-z]/g;
//         if (psw.value.match(lowerCaseLetters)) {
//             letter.classList.remove("invalid");
//             letter.classList.add("valid");
//         } else {
//             letter.classList.remove("valid");
//             letter.classList.add("invalid");
//         }
//
//         // Validate capital letters
//         var upperCaseLetters = /[A-Z]/g;
//         if (psw.value.match(upperCaseLetters)) {
//             capital.classList.remove("invalid");
//             capital.classList.add("valid");
//         } else {
//             capital.classList.remove("valid");
//             capital.classList.add("invalid");
//         }
//
//         // Validate numbers
//         var numbers = /[0-9]/g;
//         if (psw.value.match(numbers)) {
//             number.classList.remove("invalid");
//             number.classList.add("valid");
//         } else {
//             number.classList.remove("valid");
//             number.classList.add("invalid");
//         }
//
//         // Validate length
//         if (psw.value.length >= 8) {
//             length.classList.remove("invalid");
//             length.classList.add("valid");
//         } else {
//             length.classList.remove("valid");
//             length.classList.add("invalid");
//         }
//     }
//     // if ($('#psw').val()) {
//     //   $('#message_id').html('Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters').css('color', 'green');
//     // } else
//     //   $('#message_id').html('Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters').css('color', 'red');
// });


$("#job_submit").click(function () {

    // alert("Congrats! Please Ur Page Reload");
    // All academic table

    var academic_table = $('#academic_info_table_body');
    var academic_rowCount = $('#academic_info_table_body tr').length;
    var data_list_academic = [];

    for (var j = 0; j < academic_rowCount; j++) {
        var b = "tr:eq()";
        var output_academic = [b.slice(0, 6), j, b.slice(6)].join('');


        var academic_col1 = academic_table.find(output_academic).find("td:eq(1) select").val(); // get current row 1st TD
        var academic_col2 = academic_table.find(output_academic).find("td:eq(2) input[id='exam_degree_title_name']").val(); // get current row 2nd TD
        var academic_col3 = academic_table.find(output_academic).find("td:eq(3) input[id='concentration_major_group_name']").val();
        var academic_col4 = academic_table.find(output_academic).find("td:eq(4) input[id='board_name']").val();
//            var academic_col4 = academic_table.find(output_academic).find("td:eq(4) select option:selected").val();
        var academic_col5 = academic_table.find(output_academic).find("td:eq(5) input[id='institute_name']").val();
        var academic_col6 = academic_table.find(output_academic).find("td:eq(6) select option:selected").val();
        var academic_col7 = academic_table.find(output_academic).find("td:eq(7) input[id='cgpa']").val();
        var academic_col8 = academic_table.find(output_academic).find("td:eq(8) input[id='mark']").val();
        var academic_col9 = academic_table.find(output_academic).find("td:eq(9) input[id='scale']").val();
        var academic_col10 = academic_table.find(output_academic).find("td:eq(10) input[id='passing_year']").val();
        var academic_col11 = academic_table.find(output_academic).find("td:eq(11) input[id='duration']").val();
        var academic_col12 = academic_table.find(output_academic).find("td:eq(12) input[id='achievement']").val();


        var academic_data = "" + academic_col1 + "/" + academic_col2 + "/" + academic_col3 + "/" + academic_col4 + "/" + academic_col5 + "/" + academic_col6 + "/" + academic_col7 + "/" + academic_col8 + "/" + academic_col9 + "/" + academic_col10 + "/" + academic_col11 + "/" + academic_col12 + "/";

        data_list_academic.push(academic_data);

    }
    data_list_academic.join(',');
    $("input[name='academic_all_row_data']").val(data_list_academic);

//        $("input[name=academic_row]").val(academic_rowCount);


//         All experience table
    var experience_table = $('#experience_info_table_body');
    var experience_rowCount = $('#experience_info_table_body tr').length;
    var data_list_experience = [];

    for (var i = 0; i < experience_rowCount; i++) {
        var c = "tr:eq()";
        var output_experience = [c.slice(0, 6), i, c.slice(6)].join('');

        var experience_col1 = experience_table.find(output_experience).find("td:eq(1) input[id='company_name']").val(); // get current row 1st TD value
        var experience_col2 = experience_table.find(output_experience).find("td:eq(2) input[id='position']").val(); // get current row 2nd TD
        var experience_col3 = experience_table.find(output_experience).find("td:eq(3) input[id='department']").val();
        var experience_col4 = experience_table.find(output_experience).find("td:eq(4) input[id='area_experiences']").val();
        var experience_col5 = experience_table.find(output_experience).find("td:eq(5) input[id='responsibilities']").val();
        var experience_col6 = experience_table.find(output_experience).find("td:eq(6) input[id='company_location']").val();
        var experience_col7 = experience_table.find(output_experience).find("td:eq(7) input[id='start_date']").val();
        var experience_col8 = experience_table.find(output_experience).find("td:eq(8) input[id='to_date']").val();

        var experience_data = "" + experience_col1 + "/" + experience_col2 + "/" + experience_col3 + "/" + experience_col4 + "/" + experience_col5 + "/" + experience_col6 + "/" + experience_col7 + "/" + experience_col8 + "/";

        data_list_experience.push(experience_data);
    }
    data_list_experience.join(',');
    $("input[name='experience_all_row_data']").val(data_list_experience);
////        $("input[name=experience_row]").val(experience_rowCount);
//
    // All reference table
    var reference_table = $('#reference_info_table_body');
    var reference_rowCount = $('#reference_info_table_body tr').length;
    var data_list_reference = [];

    for (var k = 0; k < reference_rowCount; k++) {
        var d = "tr:eq()";
        var output_reference = [d.slice(0, 6), k, d.slice(6)].join('');

        var reference_col1 = reference_table.find(output_reference).find("td:eq(1) input[id='reference_name']").val(); // get current row 1st TD value
        var reference_col2 = reference_table.find(output_reference).find("td:eq(2) input[id='reference_organization']").val(); // get current row 2nd TD
        var reference_col3 = reference_table.find(output_reference).find("td:eq(3) input[id='reference_position']").val();
        var reference_col4 = reference_table.find(output_reference).find("td:eq(4) input[id='reference_relation']").val();
        var reference_col5 = reference_table.find(output_reference).find("td:eq(5) input[id='reference_mobile']").val();
        var reference_col6 = reference_table.find(output_reference).find("td:eq(6) input[id='reference_phone']").val();
        var reference_col7 = reference_table.find(output_reference).find("td:eq(7) input[id='reference_email']").val();
        var reference_col8 = reference_table.find(output_reference).find("td:eq(8) input[id='reference_address']").val();

        var reference_data = "" + reference_col1 + "/" + reference_col2 + "/" + reference_col3 + "/" + reference_col4 + "/" + reference_col5 + "/" + reference_col6 + "/" + reference_col7 + "/" + reference_col8 + "/";

        data_list_reference.push(reference_data);
    }
    data_list_reference.join(',');
    $("input[name='reference_all_row_data']").val(data_list_reference);
//        $("input[name=reference_row]").val(reference_rowCount);

    // All article table
    var article_table = $('#article_info_table_body');
    var article_rowCount = $('#article_info_table_body tr').length;
    var data_list_article = [];

    for (var o = 0; o < article_rowCount; o++) {
        var m = "tr:eq()";
        var output_article = [m.slice(0, 6), o, m.slice(6)].join('');

        var article_col1 = article_table.find(output_article).find("td:eq(1) input[id='article_name']").val(); // get current row 1st TD value
        var article_col2 = article_table.find(output_article).find("td:eq(2) input[id='article_author']").val();
        var article_col3 = article_table.find(output_article).find("td:eq(3) input[id='vol_no']").val();
        var article_col4 = article_table.find(output_article).find("td:eq(4) input[id='page_no']").val();
        var article_col5 = article_table.find(output_article).find("td:eq(5) input[id='article_publication_date']").val();
        var article_col6 = article_table.find(output_article).find("td:eq(6) input[id='publication_country']").val();
//            var article_col4 = article_table.find(output_article).find("td:eq(4) input[id='article_file']").val();


        var article_data = "" + article_col1 + "/" + article_col2 + "/" + article_col3 + "/" + article_col4 + "/" + article_col5 + "/" + article_col6 + "/";

        data_list_article.push(article_data);
    }
    data_list_article.join(',');
    $("input[name='article_all_row_data']").val(data_list_article);

    // All conference table
    var conference_table = $('#conference_info_table_body');
    var conference_rowCount = $('#conference_info_table_body tr').length;
    var data_list_conference = [];

    for (var o = 0; o < conference_rowCount; o++) {
        var m = "tr:eq()";
        var output_conference = [m.slice(0, 6), o, m.slice(6)].join('');

        var conference_col1 = conference_table.find(output_conference).find("td:eq(1) input[id='proceedings_name']").val(); // get current row 1st TD value
        var conference_col2 = conference_table.find(output_conference).find("td:eq(2) input[id='article_author']").val(); // get current row 2nd TD
        var conference_col3 = conference_table.find(output_conference).find("td:eq(3) input[id='page_no']").val();
        var conference_col4 = conference_table.find(output_conference).find("td:eq(4) input[id='article_publication_date']").val();
        var conference_col5 = conference_table.find(output_conference).find("td:eq(5) input[id='publication_country']").val();
//            var article_col4 = article_table.find(output_article).find("td:eq(4) input[id='article_file']").val();


        var conference_data = "" + conference_col1 + "/" + conference_col2 + "/" + conference_col3 + "/" + conference_col4 + "/" + conference_col5 + "/";

        data_list_conference.push(conference_data);
    }
    data_list_conference.join(',');
    $("input[name='conference_all_row_data']").val(data_list_conference);


    // All publication table
    var publication_table = $('#publication_info_table_body');
    var publication_rowCount = $('#publication_info_table_body tr').length;
    var data_list_publication = [];

    for (var o = 0; o < publication_rowCount; o++) {
        var m = "tr:eq()";
        var output_publication = [m.slice(0, 6), o, m.slice(6)].join('');

        var publication_col1 = publication_table.find(output_publication).find("td:eq(1) input[id='publication_name']").val(); // get current row 1st TD value
        var publication_col2 = publication_table.find(output_publication).find("td:eq(2) input[id='publisher']").val(); // get current row 2nd TD
        var publication_col3 = publication_table.find(output_publication).find("td:eq(3) input[id='year']").val();

        var publication_data = "" + publication_col1 + "/" + publication_col2 + "/" + publication_col3 + "/";

        data_list_publication.push(publication_data);
    }
    data_list_publication.join(',');
    $("input[name='publication_all_row_data']").val(data_list_publication);


    // All project table
    var project_table = $('#project_info_table_body');
    var project_rowCount = $('#project_info_table_body tr').length;
    var data_list_project = [];

    for (var o = 0; o < project_rowCount; o++) {
        var m = "tr:eq()";
        var output_project = [m.slice(0, 6), o, m.slice(6)].join('');

        var project_col1 = project_table.find(output_project).find("td:eq(1) input[id='academic_program_name']").val(); // get current row 1st TD value
        var project_col2 = project_table.find(output_project).find("td:eq(2) input[id='title']").val(); // get current row 2nd TD
        var project_col3 = project_table.find(output_project).find("td:eq(3) input[id='project_year']").val();

        var project_data = "" + project_col1 + "/" + project_col2 + "/" + project_col3 + "/";

        data_list_project.push(project_data);
    }
    data_list_project.join(',');
    $("input[name='project_all_row_data']").val(data_list_project);


    // All member table
    var member_table = $('#member_info_table_body');
    var member_rowCount = $('#member_info_table_body tr').length;
    var data_list_member = [];

    for (var o = 0; o < member_rowCount; o++) {
        var m = "tr:eq()";
        var output_member = [m.slice(0, 6), o, m.slice(6)].join('');

        var member_col1 = member_table.find(output_member).find("td:eq(1) input[id='description']").val(); // get current row 1st TD value
        var member_col2 = member_table.find(output_member).find("td:eq(2) input[id='year']").val(); // get current row 2nd TD

        var member_data = "" + member_col1 + "/" + member_col2 + "/";

        data_list_member.push(member_data);
    }
    data_list_member.join(',');
    $("input[name='member_all_row_data']").val(data_list_member);


    // All certification table
    var certification_table = $('#certification_info_table_body');
    var certification_rowCount = $('#certification_info_table_body tr').length;
    var data_list_certification = [];

    for (var o = 0; o < certification_rowCount; o++) {
        var m = "tr:eq()";
        var output_certification = [m.slice(0, 6), o, m.slice(6)].join('');

        var certification_col1 = certification_table.find(output_certification).find("td:eq(1) input[id='certification']").val(); // get current row 1st TD value
        var certification_col2 = certification_table.find(output_certification).find("td:eq(2) input[id='institute_name']").val(); // get current row 2nd TD
        var certification_col3 = certification_table.find(output_certification).find("td:eq(3) input[id='company_location']").val();
        var certification_col4 = certification_table.find(output_certification).find("td:eq(4) input[id='start_date']").val();
        var certification_col5 = certification_table.find(output_certification).find("td:eq(5) input[id='to_date']").val();
        var certification_col6 = certification_table.find(output_certification).find("td:eq(6) input[id='concentration_major_name']").val();


        var certification_data = "" + certification_col1 + "/" + certification_col2 + "/" + certification_col3 + "/" + certification_col4 + "/" + certification_col5 + "/" + certification_col6 + "/";

        data_list_certification.push(certification_data);
    }
    data_list_certification.join(',');
    $("input[name='certification_all_row_data']").val(data_list_certification);


    // All training table
    var training_table = $('#training_info_table_body');
    var training_rowCount = $('#training_info_table_body tr').length;
    var data_list_training = [];

    for (var o = 0; o < training_rowCount; o++) {
        var m = "tr:eq()";
        var output_training = [m.slice(0, 6), o, m.slice(6)].join('');

        var training_col1 = training_table.find(output_training).find("td:eq(1) input[id='title']").val(); // get current row 1st TD value
        var training_col2 = training_table.find(output_training).find("td:eq(2) input[id='institute_name']").val(); // get current row 2nd TD
        var training_col3 = training_table.find(output_training).find("td:eq(3) input[id='company_location']").val();
        var training_col4 = training_table.find(output_training).find("td:eq(4) input[id='start_date']").val();
        var training_col5 = training_table.find(output_training).find("td:eq(5) input[id='to_date']").val();
        var training_col6 = training_table.find(output_training).find("td:eq(6) input[id='concentration_major_name']").val();


        var training_data = "" + training_col1 + "/" + training_col2 + "/" + training_col3 + "/" + training_col4 + "/" + training_col5 + "/" + training_col6 + "/";

        data_list_training.push(training_data);
    }
    data_list_training.join(',');
    $("input[name='training_all_row_data']").val(data_list_training);


    // All language table
    var language_table = $('#language_info_table_body');
    var language_rowCount = $('#language_info_table_body tr').length;
    var data_list_language = [];

    for (var o = 0; o < language_rowCount; o++) {
        var m = "tr:eq()";
        var output_language = [m.slice(0, 6), o, m.slice(6)].join('');

        var language_col1 = language_table.find(output_language).find("td:eq(1) input[id='language_name']").val(); // get current row 1st TD value
        var language_col2 = language_table.find(output_language).find("td:eq(2) select option:selected").val();
        var language_col3 = language_table.find(output_language).find("td:eq(3) select option:selected").val();
        var language_col4 = language_table.find(output_language).find("td:eq(4) select option:selected").val();
        var language_col5 = language_table.find(output_language).find("td:eq(5) select option:selected").val();

        var language_data = "" + language_col1 + "/" + language_col2 + "/" + language_col3 + "/" + language_col4 + "/" + language_col5 + "/";

        data_list_language.push(language_data);
    }
    data_list_language.join(',');
    $("input[name='language_all_row_data']").val(data_list_language);


    // All award table
    var award_table = $('#award_info_table_body');
    var award_rowCount = $('#award_info_table_body tr').length;
    var data_list_award = [];

    for (var o = 0; o < award_rowCount; o++) {
        var m = "tr:eq()";
        var output_award = [m.slice(0, 6), o, m.slice(6)].join('');

        var award_col1 = award_table.find(output_award).find("td:eq(1) input[id='award']").val(); // get current row 1st TD value
        var award_col2 = award_table.find(output_award).find("td:eq(2) input[id='award_by']").val(); // get current row 2nd TD
        var award_col3 = award_table.find(output_award).find("td:eq(3) input[id='award_year']").val();


        var award_data = "" + award_col1 + "/" + award_col2 + "/" + award_col3 + "/";

        data_list_award.push(award_data);
    }
    data_list_award.join(',');
    $("input[name='award_all_row_data']").val(data_list_award);

});


$("#profile").click(function (e) {
    $("#image").click();
});

function faster(uploader) {
    if (uploader.files && uploader.files[0]) {
        $('#profile').attr('src',
            window.URL.createObjectURL(uploader.files[0]));
    }
}

$("#image").change(function () {
    faster(this);
});


$("#profileImgT").click(function (e) {
    $("#imageUpT").click();
});

function fasterPre(up) {
    if (up.files && up.files[0]) {
        $('#profileImgT').attr('src',
            window.URL.createObjectURL(up.files[0]));
    }
}

$("#imageUpT").change(function () {
    fasterPre(this);
});


//const inpFile = document.getElementById("inpFile");
//const previewContainer = document.getElementById("imagePreview");
//const previewImage = previewContainer.querySelector(".image-preview__image");
//
//inpFile.addEventListener("change", function() {
//    const file = this.files[0];
//
//    if (file) {
//       const reader = new FileReader();
//
//       previewDefaultText.style.display = "none";
//       previewImage.style.display = "block";
//
//       reader.addEventListener("load", function() {
//          previewImage.setAttribute("src", thia.result);
//       });
//
//       reader.readAsDateURL(file);
//     } else {
//       previewDefaultText.style.display = "null";
//       previewImage.style.display = "null";
//        previewImage.setAttribute("src", "");
//       }
//    }

//});


$(".foreign-box").hide();
$(".checkme").click(function () {
    if ($(this).is(":checked")) {
        $(".foreign-box").show(300);
    } else {
        $(".foreign-box").hide(200);
    }
});


function changeStatus() {
    var status = document.getElementById("result");
    if (status.value == "grade") {
        $("#mark").attr("readonly", "readonly");
        $("#cgpa").attr("readonly", false);
        $("#scale").attr("readonly", false);
    } else if (status.value == "first_division") {
        $("#mark").attr("readonly", false);
        $("#cgpa").attr("readonly", "readonly");
        $("#scale").attr("readonly", "readonly");
    } else if (status.value == "second_division") {
        $("#mark").attr("readonly", false);
        $("#cgpa").attr("readonly", "readonly");
        $("#scale").attr("readonly", "readonly");
    } else if (status.value == "third_division") {
        $("#mark").attr("readonly", false);
        $("#cgpa").attr("readonly", "readonly");
        $("#scale").attr("readonly", "readonly");
    } else if (status.value == "enrolled") {
        $("#mark").attr("readonly", "readonly");
        $("#cgpa").attr("readonly", "readonly");
        $("#scale").attr("readonly", "readonly");
    } else if (status.value == "appeared") {
        $("#mark").attr("readonly", "readonly");
        $("#cgpa").attr("readonly", "readonly");
        $("#scale").attr("readonly", "readonly");
    } else if (status.value == "awarded") {
        $("#mark").attr("readonly", "readonly");
        $("#cgpa").attr("readonly", "readonly");
        $("#scale").attr("readonly", "readonly");
    } else {
        $("#mark").attr("readonly", false);
        $("#cgpa").attr("readonly", false);
        $("#scale").attr("readonly", false);
    }
}

function changeStatusGroup() {
    var status = document.getElementById("level_of_education");
    if (status.value == "diploma") {
        $("#board_name").attr("readonly", "readonly");
    } else if (status.value == "bachelor") {
        $("#board_name").attr("readonly", "readonly");
    } else if (status.value == "masters") {
        $("#board_name").attr("readonly", "readonly");
    } else if (status.value == "phd") {
        $("#board_name").attr("readonly", "readonly");
    } else {
        $("#board_name").attr("readonly", false);
    }
}

$("#form_add_row").click(function (e) {
    var academic_info_table_main_body = document.getElementById("academic_info_table_body_row");
    var cln = academic_info_table_main_body.cloneNode(true);
    document.getElementById("academic_info_table_body").append(cln);
    var table = $('#academic_info_table_body');
    var academic_rowCount = $('#academic_info_table_body').length;


    for (var j = 0; j < academic_rowCount; j++) {
        var b = "tr:eq()";
        var output = [b.slice(0, 6), j, b.slice(6)].join('');


        table.find(output).find("td:eq(1) select[id='level_of_education']").removeAttr("selected");
        table.find(output).find("td:eq(1) select[id='level_of_education'] option:eq()").attr('selected', 'selected');
        table.find(output).find("td:eq(2) input[id='exam_degree_title_name']").val('');
        table.find(output).find("td:eq(3) input[id='concentration_major_group_name']").val('');
        table.find(output).find("td:eq(4) input[id='board_name']").val('');
        table.find(output).find("td:eq(5) input[id='institute_name']").val('');
        table.find(output).find("td:eq(6) select").removeAttr("selected");
        table.find(output).find("td:eq(6) select option:eq()").attr('selected', 'selected');
        table.find(output).find("td:eq(7) input[id='cgpa']").val('');
        table.find(output).find("td:eq(8) input[id='mark']").val('');
        table.find(output).find("td:eq(9) input[id='scale']").val('');
        table.find(output).find("td:eq(10) input[id='passing_year']").val('');
        table.find(output).find("td:eq(11) input[id='duration']").val('');
        table.find(output).find("td:eq(12) input[id='achievement']").val('');


    }

});

//##Delete Function:
$("#form_delete_row").click(function () {
    $("#academic_info_table_body").find('input[name="record"]').each(function () {
        if ($(this).is(":checked")) {
            $(this).parents("tr").remove();
//                rowUpdate = rowUpdate - 1
//                num = num - 1
//                required_master_diploma = required_master_diploma - 1
//                console.log(required_master_diploma)
        }
    });
});


$("#add_row_experience").click(function (e) {
    var experience_info_table_main_body = document.getElementById("experience_info_table_body_row");
    var cln = experience_info_table_main_body.cloneNode(true);
    document.getElementById("experience_info_table_body").append(cln);
    var table = $('#experience_info_table_body');
    var experience_rowCount = $('#experience_info_table_body').length;


    for (var j = 0; j < experience_rowCount; j++) {
        var b = "tr:eq()";
        var output = [b.slice(0, 6), j, b.slice(6)].join('');

        table.find(output).find("td:eq(1) input[id='company_name']").val('');
        table.find(output).find("td:eq(2) input[id='position']").val('');
        table.find(output).find("td:eq(3) input[id='department']").val('');
        table.find(output).find("td:eq(4) input[id='area_experiences']").val('');
        table.find(output).find("td:eq(5) input[id='responsibilities']").val('');
        table.find(output).find("td:eq(6) input[id='company_location']").val('');
        table.find(output).find("td:eq(7) input[id='start_date']").val('');
        table.find(output).find("td:eq(8) input[id='to_date']").val('');
    }


});

//##Delete Function:

$("#delete_row_experience").click(function () {
    $("#experience_info_table_body").find('input[name="record_experience"]').each(function () {
        if ($(this).is(":checked")) {
            $(this).parents("tr").remove();
//                rowUpdate = rowUpdate - 1
//                num = num - 1
//                required_master_diploma = required_master_diploma - 1
//                console.log(required_master_diploma)
        }
    });
});

$("#add_row_reference").click(function (e) {


    var reference_info_table_main_body = document.getElementById("reference_info_table_body_row");
    var cln = reference_info_table_main_body.cloneNode(true);
    document.getElementById("reference_info_table_body").append(cln);
    var table = $('#reference_info_table_body');
    var reference_rowCount = $('#reference_info_table_body').length;


    for (var j = 0; j < reference_rowCount; j++) {
        var b = "tr:eq()";
        var output = [b.slice(0, 6), j, b.slice(6)].join('');

        table.find(output).find("td:eq(1) input[id='reference_name']").val('');
        table.find(output).find("td:eq(2) input[id='reference_organization']").val('');
        table.find(output).find("td:eq(3) input[id='reference_position']").val('');
        table.find(output).find("td:eq(4) input[id='reference_relation']").val('');
        table.find(output).find("td:eq(5) input[id='reference_mobile']").val('');
        table.find(output).find("td:eq(6) input[id='reference_phone']").val('');
        table.find(output).find("td:eq(7) input[id='reference_email']").val('');
        table.find(output).find("td:eq(8) input[id='reference_address']").val('');
    }

});

//##Delete Function:

$("#delete_row_reference").click(function () {
    console.log(3)
    $('#reference_info_table_body').find('input[name="record_reference"]').each(function () {
        console.log(1)
        if ($(this).is(":checked")) {
            console.log(2)
            $(this).parents("tr").remove();
//                rowUpdate = rowUpdate - 1
//                num = num - 1
//                required_master_diploma = required_master_diploma - 1
//                console.log(required_master_diploma)
        }
    });
});

$("#add_row_article").click(function (e) {

    var article_info_table_main_body = document.getElementById("article_info_table_body_row");
    var cln = article_info_table_main_body.cloneNode(true);
    document.getElementById("article_info_table_body").append(cln);
    var table = $('#article_info_table_body');
    var article_rowCount = $('#article_info_table_body').length;


    for (var j = 0; j < article_rowCount; j++) {
        var b = "tr:eq()";
        var output = [b.slice(0, 6), j, b.slice(6)].join('');

        table.find(output).find("td:eq(1) input[id='article_name']").val('');
        table.find(output).find("td:eq(2) input[id='article_author']").val('');
        table.find(output).find("td:eq(3) input[id='vol_no']").val('');
        table.find(output).find("td:eq(4) input[id='page_no']").val('');
        table.find(output).find("td:eq(5) input[id='article_publication_date']").val('');
        table.find(output).find("td:eq(6) input[id='publication_country']").val('');

    }

});

//##Delete Function:

$("#delete_row_article").click(function () {
    console.log(3)
    $('#article_info_table_body').find('input[name="record_article"]').each(function () {
        console.log(1)
        if ($(this).is(":checked")) {
            console.log(2)
            $(this).parents("tr").remove();
//                rowUpdate = rowUpdate - 1
//                num = num - 1
//                required_master_diploma = required_master_diploma - 1
//                console.log(required_master_diploma)
        }
    });
});

$("#add_row_conference").click(function (e) {

    var conference_info_table_main_body = document.getElementById("conference_info_table_body_row");
    var cln = conference_info_table_main_body.cloneNode(true);
    document.getElementById("conference_info_table_body").append(cln);
    var table = $('#conference_info_table_body');
    var conference_rowCount = $('#conference_info_table_body').length;


    for (var j = 0; j < conference_rowCount; j++) {
        var b = "tr:eq()";
        var output = [b.slice(0, 6), j, b.slice(6)].join('');

        table.find(output).find("td:eq(1) input[id='proceedings_name']").val('');
        table.find(output).find("td:eq(2) input[id='article_author']").val('');
        table.find(output).find("td:eq(3) input[id='page_no']").val('');
        table.find(output).find("td:eq(4) input[id='article_publication_date']").val('');
        table.find(output).find("td:eq(5) input[id='publication_country']").val('');

    }

});

//##Delete Function:

$("#delete_row_conference").click(function () {
    $('#conference_info_table_body').find('input[name="record_conference"]').each(function () {
        if ($(this).is(":checked")) {
            $(this).parents("tr").remove();
//                rowUpdate = rowUpdate - 1
//                num = num - 1
//                required_master_diploma = required_master_diploma - 1
//                console.log(required_master_diploma)
        }
    });
});

$("#add_row_project").click(function (e) {

    var project_info_table_main_body = document.getElementById("project_info_table_body_row");
    var cln = project_info_table_main_body.cloneNode(true);
    document.getElementById("project_info_table_body").append(cln);
    var table = $('#project_info_table_body');
    var project_rowCount = $('#project_info_table_body').length;


    for (var j = 0; j < project_rowCount; j++) {
        var b = "tr:eq()";
        var output = [b.slice(0, 6), j, b.slice(6)].join('');

        table.find(output).find("td:eq(1) input[id='academic_program_name']").val('');
        table.find(output).find("td:eq(2) input[id='title']").val('');
        table.find(output).find("td:eq(3) input[id='project_year']").val('');
    }

});

//##Delete Function:

$("#delete_row_project").click(function () {
    $('#project_info_table_body').find('input[name="record_project"]').each(function () {
        if ($(this).is(":checked")) {
            $(this).parents("tr").remove();
//                rowUpdate = rowUpdate - 1
//                num = num - 1
//                required_master_diploma = required_master_diploma - 1
//                console.log(required_master_diploma)
        }
    });
});


$("#add_row_publication").click(function (e) {

    var publication_info_table_main_body = document.getElementById("publication_info_table_body_row");
    var cln = publication_info_table_main_body.cloneNode(true);
    document.getElementById("publication_info_table_body").append(cln);
    var table = $('#publication_info_table_body');
    var publication_rowCount = $('#publication_info_table_body').length;


    for (var j = 0; j < publication_rowCount; j++) {
        var b = "tr:eq()";
        var output = [b.slice(0, 6), j, b.slice(6)].join('');

        table.find(output).find("td:eq(1) input[id='publication_name']").val('');
        table.find(output).find("td:eq(2) input[id='publisher']").val('');
        table.find(output).find("td:eq(3) input[id='year']").val('');

    }

});

//##Delete Function:

$("#delete_row_publication").click(function () {
    $('#publication_info_table_body').find('input[name="record_publication"]').each(function () {
        if ($(this).is(":checked")) {
            $(this).parents("tr").remove();
//                rowUpdate = rowUpdate - 1
//                num = num - 1
//                required_master_diploma = required_master_diploma - 1
//                console.log(required_master_diploma)
        }
    });
});


$("#add_row_member").click(function (e) {

    var member_info_table_main_body = document.getElementById("member_info_table_body_row");
    var cln = member_info_table_main_body.cloneNode(true);
    document.getElementById("member_info_table_body").append(cln);
    var table = $('#member_info_table_body');
    var member_rowCount = $('#member_info_table_body').length;


    for (var j = 0; j < member_rowCount; j++) {
        var b = "tr:eq()";
        var output = [b.slice(0, 6), j, b.slice(6)].join('');

        table.find(output).find("td:eq(1) input[id='description']").val('');
        table.find(output).find("td:eq(2) input[id='year']").val('');

    }

});

//##Delete Function:

$("#delete_row_member").click(function () {
    $('#member_info_table_body').find('input[name="record_member"]').each(function () {
        if ($(this).is(":checked")) {
            $(this).parents("tr").remove();
//                rowUpdate = rowUpdate - 1
//                num = num - 1
//                required_master_diploma = required_master_diploma - 1
//                console.log(required_master_diploma)
        }
    });
});

$("#add_row_certification").click(function (e) {

    var certification_info_table_main_body = document.getElementById("certification_info_table_body_row");
    var cln = certification_info_table_main_body.cloneNode(true);
    document.getElementById("certification_info_table_body").append(cln);
    var table = $('#certification_info_table_body');
    var certification_rowCount = $('#certification_info_table_body').length;


    for (var j = 0; j < certification_rowCount; j++) {
        var b = "tr:eq()";
        var output = [b.slice(0, 6), j, b.slice(6)].join('');

        table.find(output).find("td:eq(1) input[id='certification']").val('');
        table.find(output).find("td:eq(2) input[id='institute_name']").val('');
        table.find(output).find("td:eq(3) input[id='company_location']").val('');
        table.find(output).find("td:eq(4) input[id='start_date']").val('');
        table.find(output).find("td:eq(5) input[id='to_date']").val('');
        table.find(output).find("td:eq(6) input[id='concentration_major_name']").val('');

    }

});

//##Delete Function:

$("#delete_row_certification").click(function () {
    console.log(3)
    $('#certification_info_table_body').find('input[name="record_certification"]').each(function () {
        console.log(1)
        if ($(this).is(":checked")) {
            console.log(2)
            $(this).parents("tr").remove();
//                rowUpdate = rowUpdate - 1
//                num = num - 1
//                required_master_diploma = required_master_diploma - 1
//                console.log(required_master_diploma)
        }
    });
});

$("#add_row_training").click(function (e) {

    var training_info_table_main_body = document.getElementById("training_info_table_body_row");
    var cln = training_info_table_main_body.cloneNode(true);
    document.getElementById("training_info_table_body").append(cln);
    var table = $('#training_info_table_body');
    var training_rowCount = $('#training_info_table_body').length;


    for (var j = 0; j < training_rowCount; j++) {
        var b = "tr:eq()";
        var output = [b.slice(0, 6), j, b.slice(6)].join('');

        table.find(output).find("td:eq(1) input[id='title']").val('');
        table.find(output).find("td:eq(2) input[id='institute_name']").val('');
        table.find(output).find("td:eq(3) input[id='company_location']").val('');
        table.find(output).find("td:eq(4) input[id='start_date']").val('');
        table.find(output).find("td:eq(5) input[id='to_date']").val('');
        table.find(output).find("td:eq(6) input[id='concentration_major_name']").val('');

    }

});

//##Delete Function:

$("#delete_row_training").click(function () {
    $('#training_info_table_body').find('input[name="record_training"]').each(function () {
        if ($(this).is(":checked")) {
            $(this).parents("tr").remove();
//                rowUpdate = rowUpdate - 1
//                num = num - 1
//                required_master_diploma = required_master_diploma - 1
//                console.log(required_master_diploma)
        }
    });
});

$("#add_row_award").click(function (e) {

    var award_info_table_main_body = document.getElementById("award_info_table_body_row");
    var cln = award_info_table_main_body.cloneNode(true);
    document.getElementById("award_info_table_body").append(cln);
    var table = $('#award_info_table_body');
    var award_rowCount = $('#award_info_table_body').length;


    for (var j = 0; j < award_rowCount; j++) {
        var b = "tr:eq()";
        var output = [b.slice(0, 6), j, b.slice(6)].join('');

        table.find(output).find("td:eq(1) input[id='award']").val('');
        table.find(output).find("td:eq(2) input[id='award_by']").val('');
        table.find(output).find("td:eq(3) input[id='award_year']").val('');

    }

});

//##Delete Function:

$("#delete_row_award").click(function () {
    console.log(3)
    $('#award_info_table_body').find('input[name="award_article"]').each(function () {
        if ($(this).is(":checked")) {
            $(this).parents("tr").remove();
//                rowUpdate = rowUpdate - 1
//                num = num - 1
//                required_master_diploma = required_master_diploma - 1
//                console.log(required_master_diploma)
        }
    });
});

$("#add_row_language").click(function (e) {

    var language_info_table_main_body = document.getElementById("language_info_table_body_row");
    var cln = language_info_table_main_body.cloneNode(true);
    document.getElementById("language_info_table_body").append(cln);
    var table = $('#language_info_table_body');
    var language_rowCount = $('#language_info_table_body').length;


    for (var j = 0; j < language_rowCount; j++) {
        var b = "tr:eq()";
        var output = [b.slice(0, 6), j, b.slice(6)].join('');

        table.find(output).find("td:eq(1) input[id='language_name']").val('');
        table.find(output).find("td:eq(2) select[id='reading']").removeAttr("selected");
        table.find(output).find("td:eq(2) select[id='reading'] option:eq()").attr('selected', 'selected');
        table.find(output).find("td:eq(2) input[id='reading']").val('');
        table.find(output).find("td:eq(3) select[id='writing']").removeAttr("selected");
        table.find(output).find("td:eq(3) select[id='writing'] option:eq()").attr('selected', 'selected');
        table.find(output).find("td:eq(3) input[id='writing']").val('');
        table.find(output).find("td:eq(4) select[id='speaking']").removeAttr("selected");
        table.find(output).find("td:eq(4) select[id='speaking'] option:eq()").attr('selected', 'selected');
        table.find(output).find("td:eq(4) input[id='speaking']").val('');
        table.find(output).find("td:eq(5) select[id='listening']").removeAttr("selected");
        table.find(output).find("td:eq(5) select[id='listening'] option:eq()").attr('selected', 'selected');
        table.find(output).find("td:eq(5) input[id='listening']").val('');

    }

});

//##Delete Function:

$("#delete_row_language").click(function () {
    $('#language_info_table_body').find('input[name="record_language"]').each(function () {
        if ($(this).is(":checked")) {
            $(this).parents("tr").remove();
//                rowUpdate = rowUpdate - 1
//                num = num - 1
//                required_master_diploma = required_master_diploma - 1
//                console.log(required_master_diploma)
        }
    });
});


$("#edu_save").click(function () {

    var base_url = window.location.origin;
    console.log(1)
    var data_edu = "?level_of_education=" + $("select[name='level_of_education']").val() + "&exam_degree_title_name=" + $("input[name='exam_degree_title_name']").val() + "&concentration_major_group_name=" + $("input[name='concentration_major_group_name']").val() + "&board_name=" + $("input[name='board_name']").val() + "&institute_name=" + $("input[name='institute_name']").val() + "&result=" + $("select[name='result']").val() + "&mark=" + $("input[name='mark']").val() + "&cgpa=" + $("input[name='cgpa']").val() + "&scale=" + $("input[name='scale']").val() + "&passing_year=" + $("input[name='passing_year']").val() + "&duration=" + $("input[name='duration']").val() + "&achievement=" + $("input[name='achievement']").val() + "&certificate=" + $("input[name='certificate']").val();
    console.log(3)
    const url_edu = base_url + '/my/jobs/account/edu' + data_edu;
    console.log(2)

    var xhttp_edu = new XMLHttpRequest();

    // xhttp_edu.onreadystatechange = function () {
    //     if (this.readyState == 4 && this.status == 200) {
    //         //Typical action to be performed when the document is ready:
    //         var response = xhttp_edu.responseText.toString().replace(/'/g, '"');
    //
    //         if (response != 'None') {
    //
    //             var x = JSON.parse(response);
    //             console.log(x['exam'])
    //             console.log(x['major'])
    //             console.log(x['institute'])
    //             console.log(x['cgpa'])
    //             console.log(x['mark'])
    //             console.log(x['scale'])
    //             console.log(x['passing_year'])
    //             console.log(x['duration'])
    //
    //
    //             $('#table_edu_body').append('<tbody><tr><td>'+ x['exam'] +'</td><td>'+ x['major'] +'</td><td>'+ x['institute'] +'</td><td>'+ x['cgpa'] +'</td><td>'+ x['mark'] +'</td><td>'+ x['scale'] +'</td><td>'+ x['passing_year'] +'</td><td>'+ x['duration'] +'</td></tr></tbody>');
    //             // $('#table_edu_body').append('#academic_info_table_body');
    //             // console.log('#academic_info_table_body')
    //             // console.log(table_edu_body)
    //             console.log(x['exam'])
    //             console.log(x['major'])
    //             console.log(x['institute'])
    //             console.log(x['cgpa'])
    //             console.log(x['mark'])
    //             console.log(x['scale'])
    //             console.log(x['passing_year'])
    //             console.log(x['duration'])


    // x.forEach(myFunction);
    //
    // function myFunction(item, index) {
    //
    // //     console.log(item['exam'])
    // }
    //         }
    //     }
    // };

    xhttp_edu.open("GET", url_edu, true);
    xhttp_edu.send();
    // location.reload();


});

$("#experience_save").click(function () {

    var base_url = window.location.origin;
    console.log(1)
    var data_list_experience = "?company_name=" + $("input[name='company_name']").val() + "&position=" + $("input[name='position']").val() + "&department=" + $("input[name='department']").val() + "&area_experiences=" + $("input[name='area_experiences']").val() + "&responsibilities=" + $("input[name='responsibilities']").val() + "&company_location=" + $("input[name='company_location']").val() + "&start_date=" + $("input[name='start_date']").val() + "&to_date=" + $("input[name='to_date']").val();
    console.log(3)
    const url_experience = base_url + '/my/jobs/account/experience' + data_list_experience;
    console.log(2)

    var xhttp_experience = new XMLHttpRequest();

    xhttp_experience.open("GET", url_experience, true);
    xhttp_experience.send();

    // location.reload('/my/jobs/account/experience');
    // location.reload();
    // alert("Congrats! Please Ur Page Reload");
});

$("#reference_save").click(function () {

    var base_url = window.location.origin;
    console.log(1)
    var data_reference = "?reference_name=" + $("input[name='reference_name']").val() + "&reference_organization=" + $("input[name='reference_organization']").val() + "&reference_position=" + $("input[name='reference_position']").val() + "&reference_relation=" + $("input[name='reference_relation']").val() + "&reference_mobile=" + $("input[name='reference_mobile']").val() + "&reference_phone=" + $("input[name='reference_phone']").val() + "&reference_email=" + $("input[name='reference_email']").val() + "&reference_address=" + $("input[name='reference_address']").val();
    console.log(3)
    const url_reference = base_url + '/my/jobs/account/reference' + data_reference;
    console.log(2)

    var xhttp_reference = new XMLHttpRequest();

    xhttp_reference.open("GET", url_reference, true);
    xhttp_reference.send();

    // alert("Congrats! Please Ur Page Reload");

    // location.reload('/my/jobs/account/reference');
    // location.reload();
});

$("#article_save").click(function () {

    var base_url = window.location.origin;
    console.log(1)
    var data_article = "?article_name=" + $("input[name='article_name']").val() + "&article_author=" + $("input[name='article_author']").val() + "&vol_no=" + $("input[name='vol_no']").val() + "&page_no=" + $("input[name='page_no']").val() + "&article_publication_date=" + $("input[name='article_publication_date']").val() + "&publication_country=" + $("input[name='publication_country']").val();
    console.log(3)
    const url_article = base_url + '/my/jobs/account/article' + data_article;
    console.log(2)

    var xhttp_article = new XMLHttpRequest();

    xhttp_article.open("GET", url_article, true);
    xhttp_article.send();

    // alert("Congrats! Please Ur Page Reload");

    // location.reload('/my/jobs/account/article');
    // location.reload();

});

$("#conference_save").click(function () {

    var base_url = window.location.origin;
    console.log(1)
    var data_conference = "?proceedings_name=" + $("input[name='proceedings_name']").val() + "&conference_author=" + $("input[name='conference_author']").val() + "&conference_page_no=" + $("input[name='conference_page_no']").val() + "&conference_article_publication_date=" + $("input[name='conference_article_publication_date']").val() + "&conference_publication_country=" + $("input[name='conference_publication_country']").val();

    const url_article = base_url + '/my/jobs/account/conference' + data_conference;
    console.log(2)

    var xhttp_article = new XMLHttpRequest();

    xhttp_article.open("GET", url_article, true);
    xhttp_article.send();

    // alert("Congrats! Please Ur Page Reload");


    // location.reload('/my/jobs/account/conference');
    // location.reload();

});

$("#training_save").click(function () {

    var base_url = window.location.origin;
    console.log(1)
    var data_training = "?training_title=" + $("input[name='training_title']").val() + "&training_institute_name=" + $("input[name='training_institute_name']").val() + "&training_company_location=" + $("input[name='training_company_location']").val() + "&training_start_date=" + $("input[name='training_start_date']").val() + "&training_to_date=" + $("input[name='training_to_date']").val() + "&training_concentration_major_name=" + $("input[name='training_concentration_major_name']").val();
    console.log(3)
    const url_training = base_url + '/my/jobs/account/training' + data_training;
    console.log(2)

    var xhttp_training = new XMLHttpRequest();

    xhttp_training.open("GET", url_training, true);
    xhttp_training.send();

    // location.reload('/my/jobs/account/training');
    // location.reload();

    // alert("Congrats! Please Ur Page Reload");

});

$("#certification_save").click(function () {

    var base_url = window.location.origin;
    console.log(1)
    var data_certification = "?certification=" + $("input[name='certification']").val() + "&degree_institute_name=" + $("input[id='degree_institute_name)']").val() + "&degree_company_location=" + $("input[id='degree_company_location)']").val() + "&degree_start_date=" + $("input[id='degree_start_date)']").val() + "&degree_to_date=" + $("input[id='degree_to_date)']").val() + "&degree_concentration_major_name=" + $("input[id='degree_concentration_major_name)']").val();
    console.log(3)
    const url_certification = base_url + '/my/jobs/account/certification' + data_certification;
    console.log(2)

    var xhttp_certification = new XMLHttpRequest();

    xhttp_certification.open("GET", url_certification, true);
    xhttp_certification.send();

    // alert("Congrats! Please Ur Page Reload");

    // location.reload('/my/jobs/account/degree');
    // location.reload();

});

$("#language_save").click(function () {

    var base_url = window.location.origin;
    console.log(1)
    var data_language = "?language_name=" + $("input[name='language_name']").val() + "&reading=" + $("select[name='reading']").val() + "&writing=" + $("select[name='writing']").val() + "&speaking=" + $("select[name='speaking']").val() + "&listening=" + $("select[name='listening']").val();
    console.log(3)
    const url_language = base_url + '/my/jobs/account/language' + data_language;
    console.log(2)

    var xhttp_language = new XMLHttpRequest();

    xhttp_language.open("GET", url_language, true);
    xhttp_language.send();

    // alert("Congrats! Please Ur Page Reload");
    // location.reload('/my/jobs/account/language');
    // location.reload();

});

$("#award_save").click(function () {

    var base_url = window.location.origin;
    console.log(1)
    var data_award = "?award=" + $("input[name='award']").val() + "&award_by=" + $("input[name='award_by']").val() + "&award_year=" + $("input[name='award_year']").val();
    console.log(3)
    const url_award = base_url + '/my/jobs/account/award' + data_award;
    console.log(2)

    var xhttp_award = new XMLHttpRequest();

    xhttp_award.open("GET", url_award, true);
    xhttp_award.send();

    // alert("Congrats! Please Ur Page Reload");

    // location.reload('/my/jobs/account/award');
    // location.reload();

});

$("#project_save").click(function () {

    var base_url = window.location.origin;
    console.log(1)
    var data_award = "?academic_program_name=" + $("input[name='academic_program_name']").val() + "&title=" + $("input[name='title']").val() + "&project_year=" + $("input[name='project_year']").val();
    console.log(3)
    const url_award = base_url + '/my/jobs/account/project' + data_award;
    console.log(2)

    var xhttp_award = new XMLHttpRequest();

    xhttp_award.open("GET", url_award, true);
    xhttp_award.send();

    // alert("Congrats! Please Ur Page Reload");

    // location.reload('/my/jobs/account/project');
    // location.reload();

});

$("#publication_save").click(function () {

    var base_url = window.location.origin;
    console.log(1)
    var data_award = "?publication_name=" + $("input[name='publication_name']").val() + "&publisher=" + $("input[name='publisher']").val() + "&year=" + $("input[name='year']").val();
    console.log(3)
    const url_award = base_url + '/my/jobs/account/book' + data_award;
    console.log(2)

    var xhttp_award = new XMLHttpRequest();

    xhttp_award.open("GET", url_award, true);
    xhttp_award.send();

    // alert("Congrats! Please Ur Page Reload");

    // location.reload('/my/jobs/account/book');
    // location.reload();

});

$("#member_save").click(function () {

    var base_url = window.location.origin;
    console.log(1)
    var data_member = "?description=" + $("input[name='description']").val() + "&member_year=" + $("input[name='member_year']").val();
    console.log(3)

    const url_member = base_url + '/my/jobs/account/member' + data_member;
    console.log(2)

    var xhttp_member = new XMLHttpRequest();

    xhttp_member.open("GET", url_member, true);
    xhttp_member.send();

    // alert("Congrats! Please Ur Page Reload");

    // location.reload('/my/jobs/account/member');
    // location.reload();

});

$("#video_save").click(function () {

    var base_url = window.location.origin;
    console.log(1)
    var data_award = "?video_resumes=" + $("input[name='video_resumes']").val() + "&demo_videos=" + $("input[name='demo_videos']").val();
    console.log(3)
    const url_award = base_url + '/my/jobs/account/video' + data_award;
    console.log(2)

    var xhttp_award = new XMLHttpRequest();

    xhttp_award.open("GET", url_award, true);
    xhttp_award.send();

});

function eduDelete(ctl) {
    var base_url = window.location.origin;
    console.log(1)
    var data_edu = "?id=" + $("input[id='xxx']").val()
    console.log($("input[id='xxx']").val())
    const url_edu = base_url + '/my/jobs/account/edu/delete' + data_edu;
    console.log(2)

    var xhttp_edu = new XMLHttpRequest();

    xhttp_edu.open("GET", url_edu, true);
    xhttp_edu.send();

    $(ctl).parents("tr").remove();

}

function articleDelete(ctl) {
    var base_url = window.location.origin;
    console.log(1)
    var data_edu = "?id=" + $("input[id='yyy']").val()
    console.log($("input[id='yyy']").val())
    const url_edu = base_url + '/my/jobs/account/article/delete' + data_edu;
    console.log(2)

    var xhttp_edu = new XMLHttpRequest();

    xhttp_edu.open("GET", url_edu, true);
    xhttp_edu.send();

    $(ctl).parents("tr").remove();

}

function conferenceDelete(ctl) {
    var base_url = window.location.origin;
    console.log(1)
    var data_edu = "?id=" + $("input[id='zzz']").val()
    console.log($("input[id='zzz']").val())
    const url_edu = base_url + '/my/jobs/account/conference/delete' + data_edu;
    console.log(2)

    var xhttp_edu = new XMLHttpRequest();

    xhttp_edu.open("GET", url_edu, true);
    xhttp_edu.send();

    $(ctl).parents("tr").remove();

}

function bookDelete(ctl) {
    var base_url = window.location.origin;
    console.log(1)
    var data_edu = "?id=" + $("input[id='aaa']").val()
    console.log($("input[id='aaa']").val())
    const url_edu = base_url + '/my/jobs/account/book/delete' + data_edu;
    console.log(2)

    var xhttp_edu = new XMLHttpRequest();

    xhttp_edu.open("GET", url_edu, true);
    xhttp_edu.send();

    $(ctl).parents("tr").remove();

}

function projectDelete(ctl) {
    var base_url = window.location.origin;
    console.log(1)
    var data_edu = "?id=" + $("input[id='bbb']").val()
    console.log($("input[id='bbb']").val())
    const url_edu = base_url + '/my/jobs/account/project/delete' + data_edu;
    console.log(2)

    var xhttp_edu = new XMLHttpRequest();

    xhttp_edu.open("GET", url_edu, true);
    xhttp_edu.send();

    $(ctl).parents("tr").remove();

}

function memberDelete(ctl) {
    var base_url = window.location.origin;
    console.log(1)
    var data_edu = "?id=" + $("input[id='ccc']").val()
    console.log($("input[id='ccc']").val())
    const url_edu = base_url + '/my/jobs/account/member/delete' + data_edu;
    console.log(2)

    var xhttp_edu = new XMLHttpRequest();

    xhttp_edu.open("GET", url_edu, true);
    xhttp_edu.send();

    $(ctl).parents("tr").remove();

}

function experienceDelete(ctl) {
    var base_url = window.location.origin;
    console.log(1)
    var data_edu = "?id=" + $("input[id='ddd']").val()
    console.log($("input[id='ddd']").val())
    const url_edu = base_url + '/my/jobs/account/experience/delete' + data_edu;
    console.log(2)

    var xhttp_edu = new XMLHttpRequest();

    xhttp_edu.open("GET", url_edu, true);
    xhttp_edu.send();

    $(ctl).parents("tr").remove();

}

function degreeDelete(ctl) {
    var base_url = window.location.origin;
    console.log(1)
    var data_edu = "?id=" + $("input[id='eee']").val()
    console.log($("input[id='eee']").val())
    const url_edu = base_url + '/my/jobs/account/degree/delete' + data_edu;
    console.log(2)

    var xhttp_edu = new XMLHttpRequest();

    xhttp_edu.open("GET", url_edu, true);
    xhttp_edu.send();

    $(ctl).parents("tr").remove();

}

function trainingDelete(ctl) {
    var base_url = window.location.origin;
    console.log(1)
    var data_edu = "?id=" + $("input[id='fff']").val()
    console.log($("input[id='fff']").val())
    const url_edu = base_url + '/my/jobs/account/training/delete' + data_edu;
    console.log(2)

    var xhttp_edu = new XMLHttpRequest();

    xhttp_edu.open("GET", url_edu, true);
    xhttp_edu.send();

    $(ctl).parents("tr").remove();

}

function awardDelete(ctl) {
    var base_url = window.location.origin;
    console.log(1)
    var data_edu = "?id=" + $("input[id='ggg']").val()
    console.log($("input[id='ggg']").val())
    const url_edu = base_url + '/my/jobs/account/award/delete' + data_edu;
    console.log(2)

    var xhttp_edu = new XMLHttpRequest();

    xhttp_edu.open("GET", url_edu, true);
    xhttp_edu.send();

    $(ctl).parents("tr").remove();

}

function languageDelete(ctl) {
    var base_url = window.location.origin;
    console.log(1)
    var data_edu = "?id=" + $("input[id='hhh']").val()
    console.log($("input[id='hhh']").val())
    const url_edu = base_url + '/my/jobs/account/language/delete' + data_edu;
    console.log(2)

    var xhttp_edu = new XMLHttpRequest();

    xhttp_edu.open("GET", url_edu, true);
    xhttp_edu.send();

    $(ctl).parents("tr").remove();

}

function referenceDelete(ctl) {
    var base_url = window.location.origin;
    console.log(1)
    var data_edu = "?id=" + $("input[id='iii']").val()
    console.log($("input[id='iii']").val())
    const url_edu = base_url + '/my/jobs/account/reference/delete' + data_edu;
    console.log(2)

    var xhttp_edu = new XMLHttpRequest();

    xhttp_edu.open("GET", url_edu, true);
    xhttp_edu.send();

    $(ctl).parents("tr").remove();

}

// function productDisplay(ctl) {
// _row = $(ctl).parents("tr");
// var cols = _row.children("td");
// $("#level_of_education").val($(cols[1]).select());
// $("#exam_degree_title_name").val($(cols[2]).text());
// $("#concentration_major_group_name").val($(cols[3]).text());
// $("#board_name").val($(cols[4]).text());
// $("#institute_name").val($(cols[5]).text);
// $("#result").val($(cols[6]).select());
// $("#cgpa").val($(cols[7]).text());
// $("#mark").val($(cols[8]).text());
// $("#scale").val($(cols[9]).text());
// $("#passing_year").val($(cols[10]).text());
// $("#duration").val($(cols[11]).text());
// $("#achievement").val($(cols[12]).text());
//
// // Change Update Button Text
// $("#edu_save").text("Update");
//
// }

// var table = document.getElementById("table").rIndex;
//
// for(var i=1; i < table.rows.length; i++){
//     table.rows[i].onclick = function() {
//         rIndex = this.rowIndex;
//         console.log(rIndex);
//         document.getElementById("level_of_education").value = this.cells[1].innerHTML;
//         document.getElementById("exam_degree_title_name").value = this.cells[2].innerHTML;
//         document.getElementById("concentration_major_group_name").value = this.cells[3].innerHTML;
//         document.getElementById("board_name").value = this.cells[4].innerHTML;
//         document.getElementById("institute_name").value = this.cells[5].innerHTML;
//         document.getElementById("result").value = this.cells[6].innerHTML;
//         document.getElementById("cgpa").value = this.cells[7].innerHTML;
//         document.getElementById("mark").value = this.cells[8].innerHTML;
//         document.getElementById("scale").value = this.cells[9].innerHTML;
//         document.getElementById("passing_year").value = this.cells[10].innerHTML;
//         document.getElementById("duration").value = this.cells[11].innerHTML;
//         document.getElementById("achievement").value = this.cells[12].innerHTML;
//     };
// }
//
// function editRow() {
//     document.getElementById("level_of_education").value = this.innerHTML;
//     document.getElementById("exam_degree_title_name").value = this.innerHTML;
//     alert('+level_of_education+' - '+exam_degree_title_name+')
//     document.getElementById("concentration_major_group_name").value = this.innerHTML;
//     document.getElementById("board_name").value = this.innerHTML;
//     document.getElementById("institute_name").value = this.innerHTML;
//     document.getElementById("result").value = this.innerHTML;
//     document.getElementById("cgpa").value = this.innerHTML;
//     document.getElementById("mark").value = this.innerHTML;
//     document.getElementById("scale").value = this.innerHTML;
//     document.getElementById("passing_year").value = this.innerHTML;
//     document.getElementById("duration").value = this.innerHTML;
//     document.getElementById("achievement").value = this.innerHTML;
// }

//
// function editTableDisplay(){
//     document.querySelector('.editTable').setAttribute('style', 'display: block;')
// }








