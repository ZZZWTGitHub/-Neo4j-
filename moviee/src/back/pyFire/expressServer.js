const { spawn } = require('child_process');
const cors = require('cors');
const path = require('path');
const iconv = require('iconv-lite');

const express = require('express');

const app = express();

app.use(cors());

app.get('/quest', (req, res) => {
  console.log('in pyFire');
  const exec = spawn('python', [
    path.join(__dirname, 'Recommend.py'),
    req.query.moviename
  ]);
  exec.stdout.on('data', data => {
    console.log('stdout: ' + iconv.decode(data, 'gbk').toString().replace(/[\n\r]/g, ''));
    res.send(iconv.decode(data, 'gbk').toString().replace(/[\n\r]/g, ''))
  });
  exec.stderr.on('data', data => {
    console.log('stderr: ' + iconv.decode(data, 'gbk'));
  });
  exec.stderr.on('close', () => {
    console.log("Closed");
  });
});

app.listen(8002, () => {
  console.log('express server(pyFire) is running at http://127.0.0.1:8002')
})