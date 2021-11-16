var express = require('express'),
  router = express.Router();

//user controllers
router.use('/api', require('./api'));


// index view
router.get('/', function(req, res) {
    res.render('index');
});

// 404 for any page that doesnt exist - This goes after all other views
router.get('*', function(req, res){
  res.status(404).send("This page doesn't exist... yet");
});


module.exports = router;