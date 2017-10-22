var uploadButton = $('#upload');

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
        $("#fileName").text(textFile.name);
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
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/api/text", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    var body = {
        "text": file
    }
    xhttp.send(body);
    var response = JSON.parse(xhttp.responseText);
    
}