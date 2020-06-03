const express = require('express');

const auth = require('./server/auth/route');
const user = require('./server/user/route');
const recipes = require('./server/recipes/route');
const nutrition = require('./server/nutrition/route');
const ingredients = require('./server/ingredients/route');

const router = express.Router(); // eslint-disable-line new-cap

router.get('/health-check', (req, res) =>
  res.send('OK')
);

router.use('/auth', auth);
router.use('/user', user);
router.use('/recipes', recipes);
router.use('/ingredients', ingredients);
router.use('/nutrition', nutrition);


module.exports = router;
