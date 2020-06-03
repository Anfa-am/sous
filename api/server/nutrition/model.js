const Promise = require('bluebird');
const mongoose = require('mongoose');
const httpStatus = require('http-status');
const APIError = require('../helpers/APIError');

mongoose.plugin(schema => { schema.options.usePushEach = true });

const NutritionSchema  = new mongoose.Schema({}, { strict: false });

NutritionSchema.method({

});

NutritionSchema.statics = {
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

module.exports = mongoose.model('Nutrition', NutritionSchema, 'nutrition');
