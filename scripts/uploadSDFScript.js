$(document).ready(
    function () {
        //when user submits sdf file and name
        $("#sdfForm").submit(
            function (e) {
                e.preventDefault(); //prevent page from refreshing on submit
                const form = $("#sdfForm")[0]; //stores file and file name

                const data = new FormData(form); //stores file and file name as form data

                //sending post request
                $.ajax({
                    data: data,
                    url: 'uploadedSDF',
                    type: 'post',
                    processData: false,
                    contentType: false,
                });

                document.getElementById("sdfForm").reset(); //reseting form

                //alerting user on valid or invalid file
                $.get("invalidFile", function (data) {
                    if (data === "invalid") {
                        $("#message").text("");
                        alert("Invalid Input");
                    }
                    else {
                        $("#message").text("Upload Successful");
                    }
                });

                $("#message").text("");
            })
    }

);
