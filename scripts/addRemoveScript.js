$(document).ready(
    function () {

        //displaying data in the elements table when user enters the page
        $.get("removedData", function (data) {
            $('#elements').children().replaceWith('<p></p>');
            var temp = data.split(",");
            for (let i = 0; i < temp.length; i++) {
                $("#elements").append("<p>" + temp[i] + "<p>");
            }
        });

        //user wants to add an element
        $("#add").click(
            function (e) {
                e.preventDefault(); //prevent page from refreshing

                //getting variables from the form
                var elementNum = $("#elementNum").val();
                var elementCode = $("#elementCode").val();
                var elementName = $("#elementName").val();
                var colors = $("#colors").val();
                var radius = $("#radius").val();
                var valid1 = false;
                var valid2 = false;
                var valid3 = false;
                var valid4 = false;
                var alertStr = "";

                //elementNum must be an int
                if ($.isNumeric(elementNum)) {
                    valid1 = true;
                }
                else {
                    alertStr += "Element Number ";
                    valid1 = false;
                }

                //element code must be 3 chars or less
                if ($.isNumeric(elementCode) === false && $.type(elementCode) === "string" && elementCode.length < 3) {
                    valid2 = true;
                }
                else {
                    alertStr += "Element code ";
                    valid2 = false;
                }

                //element name must be 32 chars or less
                if ($.isNumeric(elementName) === false && $.type(elementName) === "string" && elementName.length < 32) {
                    valid3 = true;
                }
                else {
                    alertStr += "Element Name ";
                    valid3 = false;
                }

                //must select 3 colors
                if (colors.length != 3) {
                    alertStr += "Color Selection ";
                    valid4 = false;
                }
                else {
                    valid4 = true;
                }

                alertStr += "is Invalid";

                //making sure input is valid based on above conditions
                if (valid1 == true && valid2 == true && valid3 == true && valid4 == true) {
                    //send element info to server with a post request
                    const url = "added";
                    var formData = { elementNum: elementNum, elementCode: elementCode, elementName: elementName, colors: colors, radius: radius };
                    var dataAsJSON = JSON.stringify(formData); //sending the data as JSON
                    $.post(url, dataAsJSON);

                    //sending an additional alert if the element code already exists
                    $.get("invalidElement", function (data) {
                        if (data === "invalid") {
                            alert("Element Code Already Exists");
                        }
                    });
                }
                else {
                    alert(alertStr); //input is invalid informs user 
                }

                //displaying element table when user adds an element
                $.get("removedData", function (data) {
                    $('#elements').children().replaceWith('<p></p>');
                    var temp = data.split(",");
                    for (let i = 0; i < temp.length; i++) {
                        $("#elements").append("<p>" + temp[i] + "<p>");
                    }
                });

                document.getElementById("form").reset(); //reseting form
            });

        //user wants to remove an element
        $("#remove").click(
            function (e) {

                e.preventDefault(); //prevent page from refreshing

                //getting variables from the form
                var elementNum = $("#elementNum").val();
                var elementCode = $("#elementCode").val();
                var elementName = $("#elementName").val();
                var colors = $("#colors").val();
                var radius = $("#radius").val();
                var valid1 = false;
                var valid2 = false;
                var valid3 = false;
                var valid4 = false;
                var alertStr = "";

                //elementNum must be an int
                if ($.isNumeric(elementNum)) {
                    valid1 = true;
                }
                else {
                    alertStr += "Element Number ";
                    valid1 = false;
                }

                //element code must be 3 chars or less
                if ($.isNumeric(elementCode) === false && $.type(elementCode) === "string" && elementCode.length < 3) {
                    valid2 = true;
                }
                else {
                    alertStr += "Element code ";
                    valid2 = false;
                }

                //element name must be 32 chars or less
                if ($.isNumeric(elementName) === false && $.type(elementName) === "string" && elementName.length < 32) {
                    valid3 = true;
                }
                else {
                    alertStr += "Element Name ";
                    valid3 = false;
                }

                //must select 3 colors
                if (colors.length != 3) {
                    alertStr += "Color Selection ";
                    valid4 = false;
                }
                else {
                    valid4 = true;
                }

                alertStr += "is Invalid";

                //checking if input is valid
                if (valid1 == true && valid2 == true && valid3 == true && valid4 == true) {
                    //sending valid info to server with a post request
                    const url = "removed";
                    var formData = { elementNum: elementNum, elementCode: elementCode, elementName: elementName, colors: colors, radius: radius };
                    var dataAsJSON = JSON.stringify(formData); //sending it as JSON
                    $.post(url, dataAsJSON);
                }
                else {
                    alert(alertStr); //informing user of invalid input
                }

                //displaying elements table when user removes and element
                $.get("removedData", function (data) {
                    $('#elements').children().replaceWith('<p></p>');
                    var temp = data.split(",");
                    for (let i = 0; i < temp.length; i++) {
                        $("#elements").append("<p>" + temp[i] + "<p>");
                    }
                });

                document.getElementById("form").reset(); //reseting form
            });
    }

);
