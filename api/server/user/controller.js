const User = require('./model');
const Recipe = require('../recipes/model');

function getSaves(req, res, next) {
  User.get(req.body.id).then((user) => {
    res.json({ saved: user[0].saved })
  })
}


function updateSave(req, res, next) {
  User.get(req.body.id).then((user) => {

    let resp = false
    if(user[0].saved.indexOf(req.body.index) > -1){
        user[0].saved.splice(req.body.index)
    }else{
        user[0].saved.push(req.body.index)
        resp = true
    }

    user[0].save()

    res.json({ saved: resp, saves: user[0].saved })
  })
}

function getPrefs(req, res, next) {
    User.get(req.body.id).then((user) => {
      res.json({ prefrences: user[0].prefrences })
    })
}

function updatePrefs(req, res, next) {
    const user = User.update({ _id: req.body.id }, { $set: { prefrences: req.body.prefrences } },  { multi: false }, (err, usr) => {
        res.json({success: true, user: usr})
    })
}

function getLists(req, res, next){
    User.get(req.body.id).then((user) => {
        res.json({
            groceries: user[0].groceries,
            lists: user[0].lists,
        })
    })
}

function updateGroceries(req, res, next){
    const user = User.update({ _id: req.body.id }, { $set: { groceries: req.body.groceries } },  { multi: false }, (err, usr) => {
        res.json({success: true, user: usr})
    })
}

function toggleList(req, res, next){
    User.get(req.body.id).then((user) => {
        let resp = false
        let ind = user[0].lists.indexOf(req.body.index) 

        if(ind > -1){
            user[0].lists.splice(ind, 1)
            user[0].save()
            return res.json({ saved: resp, lists: user[0].lists })
        }else{
            user[0].lists.push(req.body.index)
            resp = true
            user[0].save()
            return res.json({ saved: resp, lists: user[0].lists })
        }

  })
}

function updateList(req, res, next){ }

module.exports = {getPrefs, updatePrefs, updateSave, getSaves, getLists, updateGroceries, updateList, toggleList};
