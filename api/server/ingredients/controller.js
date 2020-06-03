const Ingredient = require('./model');


function getAll(req, res) {
  Ingredient.get(id)
    .then((lead) => {
      req.lead = lead; // eslint-disable-line no-param-reassign
      return next();
    })
    .catch(e => next(e));
}

async function ingSearch(req, res){
    let data = await Ingredient.find({ name: { $regex: req.body.query, $options: "i" } }).sort({ score: { $meta : "textScore" } }).limit(20).lean()

    return res.json(data)
}

function get(req, res) {
  return res.json(req.lead);
}

module.exports = { getAll, ingSearch };
