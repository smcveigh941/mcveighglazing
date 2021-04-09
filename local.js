// use .env file when the environment hasn't been defined.
if (process.env.ENV_DOMAIN === undefined || process.env.PROTOCOL === undefined) {
  require('dotenv').config({path: './.env'})
}

require('./index')
