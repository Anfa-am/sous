const Recipe = require('./model');

async function explorePagePopular(req, res) {
    let data = await Recipe.aggregate([ { $sample: {size: 20} }, {$match: { 'analytics.aesthtetic': { $gte: 10, $lte: 80 } } } ])
    return res.json(data)
}

async function fillTab(req, res){
    let scope = req.body.query.split(' ').map((x) => { return new RegExp(x, 'ig') })
    let data = await Recipe.find({ name: { $in : scope } }, { score : { $meta: "textScore" } }).sort({ score: { $meta : "textScore" } }).limit(20).lean()
    return res.json(data)
}

async function recipesSearch(req, res) {
    let data = await Recipe.find({ name: { $regex: req.body.query, $options: "i" } }).limit(20).lean()
    return res.json(data)
}

async function group(req, res) {
    let data = await Recipe.find({ _id: { $in : req.body.ids } })
    return res.json(data)
}

async function getSpecialTab(req, res) {
    let data = await Recipe.find(req.body.query).limit(20).lean()
    return res.json(data)
}


function get(req, res) {
  return res.json(req.lead);
}

module.exports = { explorePagePopular, recipesSearch, group, fillTab, getSpecialTab };
