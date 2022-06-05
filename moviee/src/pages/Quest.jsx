import React from 'react'
import "./RelationQuery.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch, faComment, faC } from "@fortawesome/free-solid-svg-icons";
import * as echarts from 'echarts'
import { useEffect } from 'react';

export default function Quest() {

  return (
    <>
      <div className="RelationQueryTitle"><FontAwesomeIcon icon={faComment} /> <span>Intelligent Q&#38;A</span></div>
      <div className="search">
        <div className="search-box">
          <input type="text" className="search-input" placeholder="Input the Entity you want to search..." />
          <button type="submit" className="search-btn"><FontAwesomeIcon icon={faSearch} /></button>
        </div>
      </div>
      <div id='echartsRel' style={{ width: '600px', height: '400px', top:'20px', left:'300px' }}></div>
    </>
  )
}
