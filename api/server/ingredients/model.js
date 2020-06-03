const Promise = require('bluebird');
const mongoose = require('mongoose');
const httpStatus = require('http-status');
const APIError = require('../helpers/APIError');

mongoose.plugin(schema => { schema.options.usePushEach = true });

const IngredientSchema = new mongoose.Schema({
    name: { type: String, text: true }, 
    foodGroup: { type: String, text: true }, 
    foodSubGroup: { type: String, text: true }, 
}, { strict: false });

IngredientSchema.method({

});

IngredientSchema.statics = {
  get(id) {
    return this.findById(id)
      .exec()
      .then((user) => {
        if (user) {
          return user;
        }
        const err = new APIError('No such user exists!', httpStatus.NOT_FOUND);
        return Promise.reject(err);
      });
  },

};

module.exports = mongoose.model('Ingredient', IngredientSchema, 'ingredient');
