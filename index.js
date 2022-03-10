#!/usr/bin/env node

const config = require('getconfig')
const server = require('./src/server')
const winston = require('winston')

if (config.node.env === 'production') {
  process.env.UV_THREADPOOL_SIZE = '128'
}

winston.loggers.add('logger', {
  console: {
    level: config.node.env === 'dev' ? 'debug' : 'info',
    colorize: 'true',
    label: 'category one'
  }
})

const options = {
  relativeTo: __dirname
}

server.start(options).then(() =>
    winston.loggers.get('logger').info('Server running: ', server.get().info))
