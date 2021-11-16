var express = require('express');
var router = express.Router();
var request = require('request');

try { var awsEndpoints = require('../../creds.json'); }
catch (error) { console.log(error); awsEndpoints = {};}

// Example API 1 - sum two numbers
router.post('/add', function(req, res) {
    if ( (!isNaN(req.body.num1)) && (!isNaN(req.body.num2)) ) {
        //if both params are numbers => num1 + num2
        res.json({msg: "The answer is: " + (Number(req.body.num1) + Number(req.body.num2))});
    } else {
        res.json({msg:"It looks like you included a non-number... try again."});
    }
    
});

// Example API 2 - count word frequency
router.post('/words', function(req, res) {
    var formData = {
        "url": req.body.url
    };
    request.post({url: process.env.WordFrequency || awsEndpoints.wordFrequency, form: JSON.stringify(formData)}, function (err, httpResponse, body) {
        if (!err) {
            res.json({error:false, data:JSON.parse(body)});
        } else {
            res.json({error:true, msg:"eh that link didn't work... try again."});
        }
    });
});

// Example API 3 - Check for palindrome
// helper function
//   https://medium.freecodecamp.com/how-to-reverse-a-string-in-javascript-in-3-different-ways-75e4763c68cb
function reverseString(str) {
    return str.split("").reverse().join("");
}
router.post('/palindrome', function(req, res) {
    // remove all non alphanumeric and conver to lowercase
    //   https://stackoverflow.com/questions/9364400/remove-not-alphanumeric-characters-from-string-having-trouble-with-the-char
    var word = req.body.palindromeWord.replace(/\W/g, '').toLowerCase();
    // check if string is the same if reversed
    if ( reverseString(word) == word ) {
        if (req.body.palindromeWord.length >= 2) {
            res.json({msg:"It's a palindrome!"});
        } else {
            res.json({msg:"You need a string that is at least 2 characters long... try again."});
        }
    } else {
        res.json({msg:"It's not a palindrome."});  
    }
});

module.exports = router;