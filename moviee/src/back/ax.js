import React, { Component } from 'react'
import axios from 'axios'

export default class ax extends Component {
  componentDidMount() {
   axios.get('http://127.0.0.1:8000/user?name=Four').then(res => {
     console.log(res, '++++')
   })
  }
  render() {
    return (
      <div>ax</div>
    )
  }
}
