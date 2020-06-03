const express = require('express');
const passport = require('passport');
const recipe = require('./controller');
const router = express.Router();

router.route('/specialTab/').post(recipe.getSpecialTab);
router.route('/getTab/').post(recipe.fillTab);
router.route('/group/').post(recipe.group);
router.route('/explore/').get(recipe.explorePagePopular);
router.route('/exsearch/').post(recipe.recipesSearch);

module.exports = router;
