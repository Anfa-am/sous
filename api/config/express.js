const path = require('path');
const express = require('express');
const logger = require('morgan');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const session = require('express-session');
const compress = require('compression');
const methodOverride = require('method-override');
const cors = require('cors');
const httpStatus = require('http-status');
const expressWinston = require('express-winston');
const expressValidation = require('express-validation');
const helmet = require('helmet');
const winstonInstance = require('./winston');
const routes = require('../index.route');
const config = require('./config');
const APIError = require('../server/helpers/APIError');
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;
const FacebookStrategy = require('passport-facebook').Strategy;

const User = require('../server/user/model');
const app = express();

app.use(cookieParser('***'));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use(session({
  secret: '***',
  resave: false,
  saveUninitialized: false,
  cookie: { secure: false } // Remember to set this
}));

app.use(passport.initialize());
app.use(passport.session());


app.use((req, res, next) => {
    res.locals.isAuthenticated = req.isAuthenticated()
    next()
})

if (config.env === 'development') {
  app.use(logger('dev'));
}
app.use(compress());
app.use(methodOverride());

// secure apps by setting various HTTP headers
//app.use(helmet());

// enable CORS - Cross Origin Resource Sharing
//app.use(cors());
//
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header('Access-Control-Allow-Origin', 'http://192.168.0.16:8080');
  res.header("Access-Control-Allow-Methods", "GET,HEAD,OPTIONS,POST,PUT");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization");
  res.header('Access-Control-Allow-Credentials', true);
  next();
});

// enable detailed API logging in dev env
if (config.env === 'development') {
  expressWinston.requestWhitelist.push('body');
  expressWinston.responseWhitelist.push('body');
  app.use(expressWinston.logger({
    winstonInstance,
    meta: true, // optional: log meta data about request (defaults to true)
    msg: 'HTTP {{req.method}} {{req.url}} {{res.statusCode}} {{res.responseTime}}ms',
    colorStatus: true // Color the status code (default green, 3XX cyan, 4XX yellow, 5XX red).
  }));
}


passport.serializeUser(function(user, done) {
  done(null, user);
});

passport.deserializeUser(function(user, done) {
  done(null, user);
});

passport.use(new GoogleStrategy({
    clientID: "__",
    clientSecret: "__",
    callbackURL: "http://localhost:4040/auth/google/callback"
  },
  function(accessToken, refreshToken, profile, cb) {
    User.findOrCreate(profile).then((user) => {
      return cb(null, user);
    });
  }
));

passport.use(new FacebookStrategy({
    clientID: "__",
    clientSecret: "__",
    callbackURL: "http://localhost:4040/auth/facebook/callback",
    profileFields: ['id', 'displayName', 'photos', 'email']
  }, ((accessToken, refreshToken, profile, cb) => {
      User.findOrCreate(profile).then((user) => {
        return cb(null, user);
      });
  })
));

app.use('/api', routes);
app.use('/static', express.static(path.join(__dirname, '../public')))

app.get('/auth/google', passport.authenticate('google', { scope: ['profile'] }));
app.get('/auth/google/callback', passport.authenticate('google', { failureRedirect: 'http://localhost:8080/'}), ((req, res) => {
    return res.redirect(`http://192.168.0.16:8080/#/?uid=${req.user._id}`)
}));

app.get('/auth/facebook', passport.authenticate('facebook'));
app.get('/auth/facebook/callback', passport.authenticate('facebook', {  failureRedirect: 'http://localhost:8080/', session: true  }), ((req, res) => { 
    return res.redirect(`http://192.168.0.16:8080/#/?uid=${req.user._id}`)
}));


// if error is not an instanceOf APIError, convert it.
app.use((err, req, res, next) => {
  if (err instanceof expressValidation.ValidationError) {
    // validation error contains errors which is an array of error each containing message[]
    const unifiedErrorMessage = err.errors.map(error => error.messages.join('. ')).join(' and ');
    const error = new APIError(unifiedErrorMessage, err.status, true);
    return next(error);
  } else if (!(err instanceof APIError)) {
    const apiError = new APIError(err.message, err.status, err.isPublic);
    return next(apiError);
  }
  return next(err);
});

// catch 404 and forward to error handler
app.use((req, res, next) => {
  const err = new APIError('API not found', httpStatus.NOT_FOUND);
  return next(err);
});

// log error in winston transports except when executing test suite
if (config.env !== 'test') {
  app.use(expressWinston.errorLogger({
    winstonInstance
  }));
}

// error handler, send stacktrace only during development
app.use((err, req, res, next) => // eslint-disable-line no-unused-vars
  res.status(err.status).json({
    message: err.isPublic ? err.message : httpStatus[err.status],
    stack: config.env === 'development' ? err.stack : {}
  })
);

module.exports = app;
