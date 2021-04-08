const config = require('getconfig')
// const health = require('./handlers/healthcheck')
// const info = require('./handlers/info')
// const notFound = require('./handlers/status/404')
const home = require('./handlers/home')

const GET = 'GET'
const POST = 'POST'

module.exports = [
  {
    method: GET,
    path: '/',
    handler: home.handlers().GET
  },
  {
    method: POST,
    path: '/send-message',
    handler: home.handlers().POST
  }
]
