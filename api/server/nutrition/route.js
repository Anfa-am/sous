const express = require('express');
const nutrition = require('./controller');
const router = express.Router();

router.route('/calculate/').post(nutrition.calculateStats);

module.exports = router;
