// Darber - index.js
var express = require('express');
var app = express();
var port = process.env.PORT || 3000;
var bodyParser = require('body-parser');


// Pug Tempalate Engine
require('pug');
app.set('view engine', 'pug');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

// Serve Static Files
app.use(express.static(__dirname + '/public'));

//user controllers
app.use(require('./controllers'));


app.listen(port, function() {
  console.log('Listening on port ' + port);
});
