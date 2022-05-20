import React from "react";
import { useSearchParams } from "react-router-dom";
import "./Home.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";

export default function Home() {
  // eslint-disable-next-line
  const [searchParams, setSearchParams] = useSearchParams()
  // console.log(searchParams.get('id'))
  const useID = searchParams.get('id')
  return (
    <>
      <div className="EntityQueryTitle"><FontAwesomeIcon icon={faSearch} /> <span>Entity Query</span></div>
      {/* <h2>Home of {useID}</h2> */}
      <div className="search">
        <div className="search-box">
          <input type="text" className="search-input" placeholder="Input the Entity you want to search..." />
          <button type="submit" className="search-btn"><FontAwesomeIcon icon={faSearch} /></button>
        </div>
      </div>
    </>
  )
}
