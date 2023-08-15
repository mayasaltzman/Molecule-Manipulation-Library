var options = [];
var molName = "";
var atomNum = "";
var bondNum = "";

$(document).ready(
    function () {
        $.get("addedMolecules", function (data) { //getting all molecules
            const tempArray = data.split(","); //molecules are seperated by commas, need to split them for parsing

            //getting needed info from all molecules
            for (let i = 0; i < tempArray.length; i++) {
                var temp = tempArray[i].split(" "); //split temp array by spaces to get molecule name, atom nums, and bond nums
                molName = temp[0];
                atomNum = temp[1];
                bondNum = temp[2];

                //no molecules
                if (molName === "") {
                    $('#molecule').append("<option>No Molecules</option>");
                }
                else {
                    //adding the molecule and its information to the select menu
                    $('#molecule').append("<option> Molecule: " + molName + " Atoms: " + atomNum + " Bonds: " + bondNum + "</option>");
                }
            }

            //user wants to display the selected molecule
            $("#display").click(
                function (e) {
                    e.preventDefault(); //prevent page from refreshing

                    var selected = $("#molecule").val(); //getting the value of the selected statement
                    const selectSplit = selected.split(" "); //splitting selected statement by spaces to access just the molecule  name
                    const name = selectSplit[1]; //getting the molecule name

                    //no molecules
                    if (name === "Molecules") {
                        alert("Could not display empty molecule");
                    }
                    else {
                        //getting the SVG with a post request
                        const url = "displayMol";
                        var formData = { molName: name };
                        var dataAsJSON = JSON.stringify(formData);
                        $.post(url, dataAsJSON, function (data, status) {
                            //displaying the SVG and making sure new SVGS replace the old SVG
                            $('#svg').children().replaceWith('<div></div>');
                            $("#svg").append(data);
                        });

                        //appending buttons to rotate the molecule
                        $('#rotations').children().replaceWith('<p></p>');
                        var button1 = $('<button>');
                        button1.attr('id', 'x');
                        button1.text('X Rotation');
                        var button2 = $('<button>')
                        button2.attr('id', 'y');
                        button2.text('Y Rotation');
                        var button3 = $('<button>')
                        button3.text('Z Rotation');
                        button3.attr('id', 'z');
                        $("#rotations").append(button1);
                        $("#rotations").append(button2);
                        $("#rotations").append(button3);

                        //user wants to rotate x
                        $("#x").click(
                            function (e) {
                                e.preventDefault(); //prevent page from refreshing
                                const url = "xRotation";
                                var formData = { name: name };
                                var dataAsJSON = JSON.stringify(formData);
                                $.post(url, dataAsJSON, function (data, status) {
                                    //displaying the SVG and making sure new SVGS replace the old SVG
                                    $('#svg').children().replaceWith('<div></div>');
                                    $("#svg").append(data);
                                });
                            });

                        //user wants to rotate y
                        $("#y").click(
                            function (e) {
                                e.preventDefault(); //prevent page from refreshing
                                const url = "yRotation";
                                var formData = { name: name };
                                var dataAsJSON = JSON.stringify(formData);
                                $.post(url, dataAsJSON, function (data, status) {
                                    //displaying the SVG and making sure new SVGS replace the old SVG
                                    $('#svg').children().replaceWith('<div></div>');
                                    $("#svg").append(data);
                                });
                            });

                        //user wants to rotate z
                        $("#z").click(
                            function (e) {
                                e.preventDefault(); //prevent page from refreshing
                                const url = "zRotation";
                                var formData = { name: name };
                                var dataAsJSON = JSON.stringify(formData);
                                $.post(url, dataAsJSON, function (data, status) {
                                    //displaying the SVG and making sure new SVGS replace the old SVG
                                    $('#svg').children().replaceWith('<div></div>');
                                    $("#svg").append(data);
                                });
                            });
                    }


                });

        });
    }

);

