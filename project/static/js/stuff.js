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

tweeets = [];
scores = [];

$("#updateChart").on('click', updateChart);

$("#tweets").on('click', function () {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/api/trump", true);
    xhttp.send();
    scores = [];

    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == XMLHttpRequest.DONE) {
            var tweets = JSON.parse(xhttp.responseText);
            for (tweet in tweets) {
                var xhttp2 = new XMLHttpRequest();
                var twt = tweets[tweet]
                console.log(twt)
                var temp_tweet = {
                    x: tweet,
                    tweet: twt,
                };
                tweeets.push(temp_tweet);
                $("#tweettext").append("<li>" + twt + "</li>");
                makeRequest('GET', "/api/message?message=" + twt)
                .then(function (datums) {
                  var data = JSON.parse(datums);
                  var documents = data.documents;
                  var close = datums.split("score")[1].split("id")[0];
                  var score = parseFloat(close.substring(3, close.length - 3));
                  // $("#tweettext").append("<h2> " + score + "</h2>");
                  scores.push(score);
                  tweeets[scores.length - 1].y = score;
                });
            }
        }
    }
});

function updateChart() {
    var chart = angular.element( document.querySelector( '#myChart' ) )[0].getContext('2d');
    chart.height = 1000;
    var newChart = new Chart(chart, {
       type: 'scatter',
       data: {
          datasets: [{
             data: tweeets
          }]
       },
       options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                   xAxes: [{
      type: 'linear',
      position: 'bottom'
    }]
                 },
            title: {
                display: true,
                text: "Trump Tweets",
                fontSize: 40,
                fontFamily: 'Open Sans',
            },
            tooltips: {
                callbacks: {
                    label: function(tooltipItem, chartData) {
                        return tweeets[tooltipItem['index']]['tweet'];
                    }
                }
            },
            legend: {
                display: false,
            }
        }
    });
    console.log(newChart);
    console.log(tweeets);
}

function makeRequest (method, url) {
  return new Promise(function (resolve, reject) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url);
    xhr.onload = function () {
      if (this.status >= 200 && this.status < 300) {
        resolve(xhr.response);
      } else {
        reject({
          status: this.status,
          statusText: xhr.statusText
        });
      }
    };
    xhr.onerror = function () {
      reject({
        status: this.status,
        statusText: xhr.statusText
      });
    };
    xhr.send();
  });
}


$("#sub").on('click', getData);

function getData() {
  var username = $('#username').val();
  var recipient = $('#recipient').val();
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/api/text/?username=" + username + "&recipient=" + recipient, true);
  xhttp.send();
  console.log(xhttp.responseType);
  //JSON.parse(xhttp.responseText);
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

