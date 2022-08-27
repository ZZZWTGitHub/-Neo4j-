var mysql = require('mysql');

const authInfo = {
  host : 'localhost',
  user : 'root',
  password : '123456',
  port: '3306',
  database : 'moviee'
};

async function queryMovie(name, callback) {
  const connection = await mysql.createConnection(authInfo);
  connection.connect();
  // 创建查询语句connection
  const sql = `SELECT * FROM movie WHERE movie_name LIKE '%${name}%' LIMIT 10`;

  connection.query(sql, (err, res) => {

    //打印错误信息
    if (err) {
      callback(`[SELECT ERROR] - ${err.message}`);
    }


    //打印查询结果
    else {
      callback(res);
    }
  });
  connection.end();
}

module.exports = {
  queryMovie
};