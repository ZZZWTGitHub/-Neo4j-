const { spawn } = require('child_process');
const cors = require('cors');
const path = require('path');

const express = require('express');

const app = express();

app.use(cors());

app.get('/movie', (req, res) => {
  console.log('in pyFire');
  const exec = spawn('python', [path.join(__dirname, 'test.py')]);
  exec.stdout.on('data', data => {
    console.log('stdout: ' + data);
  });
  exec.stderr.on('data', data => {
    console.log('stderr: ' + data);
  });
  exec.stderr.on('close', () => {
    console.log("Closed");
  });
});

app.listen(8002, () => {
  console.log('express server(pyFire) is running at http://127.0.0.1:8002')
})