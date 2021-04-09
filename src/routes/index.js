const register = async server => {
  const protectedRoutes = require('./routes')
  const publicRoutes = require('./public')

  server.route(protectedRoutes)
  server.route(publicRoutes)
}

exports.plugin = {
  register,
  name: 'routes',
  version: '1.0.0'
}
