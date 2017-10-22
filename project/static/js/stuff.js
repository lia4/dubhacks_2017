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

function updateChart(datas) {
    var chart = angular.element( document.querySelector( '#myChart' ) )[0].getContext('2d');
    chart.height = 1000;
    var scatterChart = new Chart(chart, {
    type: 'scatter',
    data: {
        datasets: [{
            label: 'Scatter Dataset',
            data: datas
        }]
    },
    options: {
        elements: {
          line: {
            tension: 0,
            fill: 'false'
          }
        },
        scales: {
            xAxes: [{
                type: 'linear',
                position: 'bottom'
            }]
        }
    }
});
}


$("#sub").on('click', getData);

function getData() {
  var username = $('#username').val();
  var recipient = $('#recipient').val();
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/api/text/?username=" + username + "&recipient=" + recipient, false);
  xhttp.send();
  var data = JSON.parse(xhttp.responseText);
  var plot_data = data.results.map(function(result) {
    var x = result.key[2];
    var y = result.value.documents[0].score;
    return {"x": x, "y": y};
  });
  updateChart(plot_data);
}

function processFile(e) {
    var username = $('#username').val();
    var recipient = $('#recipient').val();
    console.log("Processing file");
    var file = e.target.result;
    $("#fileName").text(name);
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/api/text/?username=" + username + "&recipient=" + recipient, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(JSON.stringify(file));
    console.log("success");
}

