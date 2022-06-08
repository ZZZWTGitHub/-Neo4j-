const query = require('./query')
const cors = require('cors')

const express = require('express')

const app = express()

app.use(cors())

app.get('/movie', (req, res) => {
  console.log('-----------')
  console.log('moviename:', req.query.name)
  // console.log(req.query.age)
  // console.log(req.query.gender)
  query.queryMovie(req.query.name).then((result) => {
    res.send(result)
  })
})

app.get('/moviedetail', (req, res) => {
  console.log('moviedetail', req.query.movietitle)
  query.queryMovieDetail(req.query.movietitle).then((result) => {
    res.send(result)
  })
})

app.listen(8000, () => { 
  console.log('express server is running at http://127.0.0.1:8000')
})