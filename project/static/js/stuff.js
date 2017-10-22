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


$("#tweets").on('click', function () {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/api/trump", true);
    xhttp.send();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == XMLHttpRequest.DONE) {
            var tweets = JSON.parse(xhttp.responseText);
            for (tweet in tweets) {
                var xhttp2 = new XMLHttpRequest();
                xhttp2.open("GET", "/api/message?message=" + tweets[tweet], true);
                xhttp2.setRequestHeader("Content-type", "application/json");
                xhttp2.send();
                while (true) {
                    if (xhttp2.readyState == XMLHttpRequest.DONE) {
                        var score = JSON.parse(xhttp2.responseText);
                        console.log(score);
                    }
                }
                $("#tweettext").append("<li>" + tweets[tweet] + "</li>");
            }
        }
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