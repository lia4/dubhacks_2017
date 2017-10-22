var uploadButton = $('#upload');
var name;
$(document).on('change', '#file', function() {
    if (!window.FileReader) {
        alert('Your browser is not supported');
        return false;
    }
    var input = $('#file').get(0);

    // Create a reader object
    var reader = new FileReader();
    if (input.files.length) {
        var textFile = input.files[0];
        console.log(textFile.name);
        name = textFile.name;
        $("#fileName").text("Loading...");
        // Read the file
        reader.readAsText(textFile);
        // When it's loaded, process it
        $(reader).on('load', processFile);
    } else {
        alert('Please upload a file before continuing')
    } 
});

function processFile(e) {
    console.log(e);
    console.log("Processing file");
    var file = e.target.result;
    console.log(file);
    $("#fileName").text(name);
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/api/text", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(JSON.stringify(file));
    // var response = JSON.parse(xhttp.responseText);
    
}