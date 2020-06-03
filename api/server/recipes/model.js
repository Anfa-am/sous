const Promise = require('bluebird');
const mongoose = require('mongoose');
const httpStatus = require('http-status');
const APIError = require('../helpers/APIError');

mongoose.plugin(schema => { schema.options.usePushEach = true });

const RecipeSchema  = new mongoose.Schema({
    name: { type: String, text: true }, 
    ingredients: { type: Array, text: true }, 

}, { strict: false });

RecipeSchema.method({

});

RecipeSchema.statics = {
  get(id) {
    return this.find({_id: id}).exec().then((user) => {
        if (user) {
          return user;
        }
        const err = new APIError('No such user exists!', httpStatus.NOT_FOUND);
        return Promise.reject(err);
      });
  },

};

module.exports = mongoose.model('Recipe', RecipeSchema, 'recipe');
