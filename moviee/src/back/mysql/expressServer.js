// 导入一系列依赖
const cors = require('cors');
const express = require('express');
const query = require('./query');

// 实例化express
const app = express();

// 跨域中间件
app.use(cors());

// 监听/movie
app.get('/movie', (req, res) => {
  // console.log('-----------');
  // console.log('moviename:', req.query.name);
  query.queryMovie(req.query.name.toString().replace(/[\']/g, ''), result => {
    res.send(result);
    // console.log(22222);
    console.log(result);
  });
});

// 运行于8001端口，运行前请查看是否被占用
app.listen(8001, () => { 
  console.log('express server(mysql) is running at http://127.0.0.1:8001');
})