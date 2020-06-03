const express = require('express');
const userCtrl = require('./controller');
const router = express.Router(); // eslint-disable-line new-cap

router.route('/getSaves').post(userCtrl.getSaves)

router.route('/getPrefrences').post(userCtrl.getPrefs)
router.route('/prefrences').post(userCtrl.updatePrefs)

router.route('/save').post(userCtrl.updateSave);

router.route('/getLists').post(userCtrl.getLists);
router.route('/updateGroceries').post(userCtrl.updateGroceries);
router.route('/addList').post(userCtrl.toggleList);
router.route('/updateList').post(userCtrl.updateList);

module.exports = router;
