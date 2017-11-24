const path = require('path');
const rootPath = path.normalize(__dirname + '/..');
const env = process.env.NODE_ENV || 'development';

const config = {
  development: {
    root: rootPath,
    app: {
      name: 'gutenberg-webapp'
    },
    port: process.env.PORT || 3001,
    db: 'mongodb://localhost/didercamilo'
    //db: 'mongodb://didercamilo:camilodider@localhost/didercamilo'
  },

  test: {
    root: rootPath,
    app: {
      name: 'gutenberg-webapp'
    },
    port: process.env.PORT || 3001,
    //db: 'mongodb://localhost/didercamilo'
    db: 'mongodb://didercamilo:camilodider@localhost/didercamilo'
  },

  production: {
    root: rootPath,
    app: {
      name: 'gutenberg-webapp'
    },
    port: process.env.PORT || 3001,
    //db: 'mongodb://localhost/didercamilo'
    db: 'mongodb://didercamilo:camilodider@localhost/didercamilo'
  }
};

module.exports = config[env];
