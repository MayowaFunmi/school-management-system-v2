$(document).ready(function() {

    // calculate age from date of birth

    $("#div_age").hide();
    $("#date_of_birth").focusout(function() {
        var userDate = new Date($("#date_of_birth").val());
        if (userDate == 'Invalid Date') {
            alert('Date is invalid. Provide a valid date');
        } else {
            let dd = String(userDate.getDate()).padStart(2, '0');
            let mm = String(userDate.getMonth() + 1).padStart(2, '0'); //January is 0!
            let yyyy = userDate.getFullYear();
            userDate = yyyy + '-' + mm + '-' + dd
            calculateAge(userDate);
        }
    });

    function calculateAge(userDate) {
        let ageDiff = Date.now() - new Date(userDate).getTime();
        let ageDate = new Date(ageDiff);
        let calcAge = Math.abs(ageDate.getUTCFullYear() - 1970)
        $("#age").attr('readonly', 'true');
        $("#age").val(calcAge);
        $("#div_age").show();
    };

    // calculate age from date of birth for update profile

    $("#update_date_of_birth").focusout(function() {
        var userDateUpdate = new Date($("#update_date_of_birth").val());
        if (userDateUpdate == 'Invalid Date') {
            alert('Date is invalid. Provide a valid date');
        } else {
            let dd = String(userDateUpdate.getDate()).padStart(2, '0');
            let mm = String(userDateUpdate.getMonth() + 1).padStart(2, '0'); //January is 0!
            let yyyy = userDateUpdate.getFullYear();
            userDateUpdate = yyyy + '-' + mm + '-' + dd
            calculateUpdateAge(userDateUpdate);
        }
    });

    function calculateUpdateAge(userDateUpdate) {
        let ageDiff = Date.now() - new Date(userDateUpdate).getTime();
        let ageDate = new Date(ageDiff);
        let calcAge = Math.abs(ageDate.getUTCFullYear() - 1970)
        $("#update_age").attr('readonly', 'true');
        $("#update_age").val(calcAge);
    };


    // calculate years for number of service year

    $("#service_year").hide();
    $("#first_appointment").focusout(function() {
        var serviceDate = new Date($("#first_appointment").val());
        if (serviceDate == 'Invalid Date') {
            alert('Date is invalid. Provide a valid date');
        } else {
            let dd = String(serviceDate.getDate()).padStart(2, '0');
            let mm = String(serviceDate.getMonth() + 1).padStart(2, '0'); //January is 0!
            let yyyy = serviceDate.getFullYear();
            serviceDate = yyyy + '-' + mm + '-' + dd
            calculateServiceAge(serviceDate);
        }
    });

    function calculateServiceAge(serviceDate) {
        let ageDiff = Date.now() - new Date(serviceDate).getTime();
        let ageDate = new Date(ageDiff);
        let calcAge = Math.abs(ageDate.getUTCFullYear() - 1970)
        $("#years_in_service").attr('readonly', 'true');
        $("#years_in_service").val(calcAge);
        $("#service_year").show();
    };


    // calculate years for number of service year update

    $("#update_first_appointment").focusout(function() {
        var serviceDateUpdate = new Date($("#update_first_appointment").val());
        if (serviceDateUpdate == 'Invalid Date') {
            alert('Date is invalid. Provide a valid date');
        } else {
            let _dd = String(serviceDateUpdate.getDate()).padStart(2, '0');
            let _mm = String(serviceDateUpdate.getMonth() + 1).padStart(2, '0'); //January is 0!
            let _yyyy = serviceDateUpdate.getFullYear();
            serviceDateUpdate = _yyyy + '-' + _mm + '-' + _dd
            calculateServiceAgeUpdate(serviceDateUpdate);
        }
    });

    function calculateServiceAgeUpdate(serviceDateUpdate) {
        let _ageDiff = Date.now() - new Date(serviceDateUpdate).getTime();
        let _ageDate = new Date(_ageDiff);
        let _calcAge = Math.abs(_ageDate.getUTCFullYear() - 1970)
        $("#update_years_in_service").attr('readonly', 'true');
        $("#update_years_in_service").val(_calcAge);
    };

    // display schools by selected zone
    $('#current_posting_zone').focusout(function() {
        $(".current_posting_school").empty();
        var selectedZoneId = $('#current_posting_zone option:selected').val()
        $.ajax({
            url: '/auths/get_school_by_zone/',
            data: {
                'selected_zone_id': selectedZoneId
            },
            dataType: 'json',
            success: function(schools) {
                $('.current_posting_school').append(schools.data)
            }
        });
    });
    // add multiple images new
    var maxField = 20; // input fields increment limitation
    //var addButton = $('.add_button'); // add button selector
    var images = $('#images'); // input field wrapper
    var fieldHTML = `
    <div>
        <input name='document_title[]' type="text" value="" class="form-control" placeholder="Add Name OF Document">
        <input type="file" name="documents">
        <i class="fa fa-times close_btn"></i>
    </div>
    <br>`
        //  onchange="showPreview(event);
    var x = 1

    $('input#add_image').on('click', function(e) {
        e.preventDefault()
            // check maximum number of input fields
        if (x < maxField) {
            images.append(fieldHTML);
            x++
        }
    });

    $(images).on('click', '.close_btn', function(e) {
        e.preventDefault()
        $(this).parent('div').remove()
        x--
    });

    function showPreview(event) {
        console.log('working')
        if (event.target.files.length > 0) {
            var src = URL.createObjectURL(event.target.files[0]);
            var preview = $('#preview')
            preview.src = src;
            preview.style.display = 'block'
        }
    }

    // display button for zones and schools in update profile
    $('button#show_zone').click(function(e) {
        e.preventDefault()
        $('#current_posting_zone').show()
        $('.current_posting_school').show()
    });

})