$(document).ready(function() {
    var searchFields = $(".search_fields")
    var searcHTML = `
        <select name="column_1" class="column_1">
            <h2>Teachers' data to display:</h2>
            <option value="user_id">Username</option>
            <option value="gender">Gender</option>
            <option value="date_of_birth">Date Of Birth</option>
            <option value="age">Age</option>
            <option value="religion">Religion</option>
            <option value="created_date">Registered Date</option>
            <option value="designation">Designation</option>
            <option value="grade_level">Grade/Level</option>
            <option value="first_appointment">First Appointment Date</option>
            <option value="qualification">Qualification</option>
            <option value="years_in_service">Years In Service</option>
            <option value="discipline">Discipline</option>
            <option value="current_posting_zone_id">Zone</option>
            <option value="current_posting_school_id">School</option>
            <option value="current_subject_id">Subject</option>
        </select>
    `

    $('button#add_field').on('click', function(e) {
        e.preventDefault()
        searchFields.append(searcHTML)
    });

    $('form#stats_form').on('submit', function(e) {
        e.preventDefault()
            //var fields = $('#column_1 option:selected').val()
            //var select = $('select[name="column_1[]"]').val()
        $(".show_table").empty();
        var fields = $('.column_1').map(function() {
            return this.value;
        }).get()
        console.log(fields)
        $.ajax({
            url: '/stats/get_table_data/',
            data: {
                'fields': fields
            },
            dataType: 'json',
            success: function(teacher_html) {
                console.log(teacher_html.data)
                $('.show_table').append(teacher_html.data)
            }
        });
    })
})