import React from "react";
import { useSearchParams } from "react-router-dom";

export default function Home() {
  // eslint-disable-next-line
  const [searchParams, setSearchParams] = useSearchParams()
  console.log(searchParams.get('id'))
  const useID = searchParams.get('id')
  return (
    <h2>Home of {useID}</h2>
  )
}
