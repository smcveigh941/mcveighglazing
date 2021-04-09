module.exports = [
  {
    method: 'GET',
    path: '/public/{param*}',
    handler: {
      directory: {
        path: 'public/',
        listing: false
      }
    }
  },
  {
    method: 'GET',
    path: '/{param*}',
    handler: {
      directory: {
        path: 'robots/',
        listing: false
      }
    }
  }
]
