const glue = require('@hapi/glue')
const logger = require('winston').loggers.get('logger')
const manifest = require('./manifest')

let server

const startServer = async (options) => {
  try {
    server = await glue.compose(manifest, options)
    server.views(require('./views'))
    await server.start()
  } catch (err) {
    logger.error(err)
    process.exit(1)
  }
}

module.exports = {
  start: startServer,
  get: () => {
    return server
  }
}
