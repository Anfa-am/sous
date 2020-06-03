const Nutrition = require('./model');

async function calculateStats(req, res) {
    let scope = req.body.ingredient.split(' ').map((x) => { return new RegExp(x) })

    let test = await Nutrition.aggregate(
      [{ $facet: {
            fat: [ { $match : { description : {$in: scope} } }, { $unwind : "$nutrients" }, { $match : { 'nutrients.description' : /fat/ig } }, { $group : { _id : "$description", fat : { $sum : "$nutrients.amountPer100G" } } }, { $sort : { fat : -1 } }, { $limit : 1 } ],
            protein: [ { $match : { description : {$in: scope} } }, { $unwind : "$nutrients" }, { $match : { 'nutrients.description' : /protein/ig } }, { $group : { _id : "$description", protein: { $sum : "$nutrients.amountPer100G" } } }, { $sort : { protein : -1 } }, { $limit : 1 } ],
            carbs: [ { $match : { description : new RegExp(req.body.ingredient) } }, { $unwind : "$nutrients" }, { $match : { 'nutrients.description' : /carb/ig } }, { $group : { _id : "$description", carbs : { $sum : "$nutrients.amountPer100G" } } }, { $sort : { carbs : -1 } }, { $limit : 1 } ],
          }
      }]
    )

    res.json(test);
}

function get(req, res) {
  return res.json(req.lead);
}

module.exports = { calculateStats };
