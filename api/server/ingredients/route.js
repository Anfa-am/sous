const express = require('express');
const nutrition = require('./controller');
const router = express.Router();

router.route('/list/').post(nutrition.getAll);
router.route('/ingsearch').post(nutrition.ingSearch);

module.exports = router;
