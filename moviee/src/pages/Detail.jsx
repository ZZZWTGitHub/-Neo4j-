import React from 'react'
import { useSearchParams } from 'react-router-dom'

export default function Detail() {
  // eslint-disable-next-line
  const [searchParams, setSearchParams] = useSearchParams()
  const thingToSearch = searchParams.get('thing')
  return (
    <>
      <h2>Detail</h2>
      <p>thingToSearch is {thingToSearch}</p>
    </>
  )
}
