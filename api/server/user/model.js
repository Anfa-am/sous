const Promise = require('bluebird');
const mongoose = require('mongoose');
const httpStatus = require('http-status');
const APIError = require('../helpers/APIError');

mongoose.plugin(schema => { schema.options.usePushEach = true });

const UserSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true
  },

  profileId: {
    type: String,
    required: true
  },

  profilePicture: {
    type: String,
    required: false,
    default: null
  },

  prefrences: {
      type: Array,
      required: false,
      default: []
  },

  saved: {
    type: Array,
    require: false,
    default: []
  },

  groceries: {
    type: Array,
    require: false,
    default: []
  },

  lists: {
    type: Array,
    require: false,
    default: []
  }

});

UserSchema.method({

});

UserSchema.statics = {
  get(id) {
    return this.find({_id: id}).exec().then((user) => {
        if (user) {
          return user;
        }
        const err = new APIError('No such user exists!', httpStatus.NOT_FOUND);
        return Promise.reject(err);
      });
  },

  list({ skip = 0, limit = 50 } = {}) {
    return this.find()
      .sort({ createdAt: -1 })
      .skip(+skip)
      .limit(+limit)
      .exec();
  },

 findById(id) {
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

  //is logged in
  //current user
 
  findOrCreate(profile) {
    return this.findOne({ "profileId": profile.id }).exec().then((user) => {
        if (user) {
          return user;
        }else{
            return this.create({
                "name": profile.displayName,
                "profileId": profile.id,
                "profilePicture": profile.photos[0] ? profile.photos[0].value : null,
            }, (newUser) => {
                return user;
            })
        }
      }
    )
  }

};

module.exports = mongoose.model('User', UserSchema);
