const config = require('getconfig')

const plugins = [
  {plugin: '@hapi/vision'},
  {plugin: '@hapi/inert'}
]

// always register user-defined plugins last; they might depend on the common ones
plugins.push({plugin: './src/routes/index'})

module.exports = {
  server: {
    port: config.connection.port
  },
  register: {
    plugins: plugins
  }
}
