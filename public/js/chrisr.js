//chrisr.js

function addApi() {
    var data = {
        num1: document.getElementById("num1").value,
        num2: document.getElementById("num2").value
        };
    $.ajax({
        type: "POST",
        url: '/api/add',
        data: data,
        success: function(result) {
            document.getElementById("sumResult").innerHTML = result.msg;
        }
    });
}

function wordApi() {
    //show loader
    $("#wordloader").removeClass('hidden');
    document.getElementById("wordResult").innerHTML = "";
    var data = {
        url: document.getElementById("url").value
        };
    //call aws
    $.ajax({
        type: "POST",
        url: '/api/words',
        data: data,
        success: function(result) {
            //hide loader
            $("#wordloader").addClass('hidden');
            if (result.data.errorMessage) {
                document.getElementById("wordResult").innerHTML = "There was an error with that URL... try again.";
            } else {
                document.getElementById("wordResult").innerHTML = "URL: <strong>"+ data.url + "</strong><br><br>" +
                    "Total words: <strong>" + result.data.count.total +
                    "</strong>.<br>Total unique words: <strong>" + result.data.count.unique +
                    "</strong>.<br><br>Most used word: <strong>" + result.data.top.word + "</strong> with <strong>" +
                    result.data.top.count + "</strong> instances.";
            }
        }    
    });
}

function palindromeApi() {
    var data = {
        palindromeWord: document.getElementById("palindromeWord").value
        };
    $.ajax({
        type: "POST",
        url: '/api/palindrome',
        data: data,
        success: function(result) {
            document.getElementById("palindromeResult").innerHTML = result.msg;
        }
    });
}

$( document ).ready(function() {
    //document ready
});