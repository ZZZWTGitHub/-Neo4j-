import React from 'react'
import "./List.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";

export default function List() {
  return (
    <>
      <div className="RelationQueryTitle"><FontAwesomeIcon icon={faSearch} /> <span>Relation Query</span></div>
      <div className="search">
        <div className="search-box">
          <input type="text" className="search-input" placeholder="Input the Entity you want to search..." />
          <button type="submit" className="search-btn"><FontAwesomeIcon icon={faSearch} /></button>
        </div>
      </div>
    </>
  )
}
