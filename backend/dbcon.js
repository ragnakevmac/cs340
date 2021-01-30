var mysql = require('mysql');
var pool = mysql.createPool({
  connectionLimit : 10,
  host            : 'classmysql.engr.oregonstate.edu',
  user            : 'cs340_macandok',
  password        : '',
  database        : 'cs340_macandok'
});

module.exports.pool = pool;