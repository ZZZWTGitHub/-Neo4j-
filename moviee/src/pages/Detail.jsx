import React from 'react'
import { useParams } from 'react-router-dom'

export default function Detail() {
  const {id} = useParams()
  return (
    <>
      <h2>Detail</h2>
      <p>detail is {id}</p>
    </>
  )
}
