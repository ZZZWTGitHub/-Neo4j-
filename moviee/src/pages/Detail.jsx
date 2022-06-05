import React from 'react'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBookOpen } from "@fortawesome/free-solid-svg-icons";
import * as echarts from 'echarts'
import { useEffect } from 'react';
import { useSearchParams } from "react-router-dom"; 

export default function Detail() {
  // eslint-disable-next-line
  const [searchParams, setSearchParams] = useSearchParams()
  const useID = searchParams.get('movietitle')
  console.log(useID)
  return (
    <>
      <div className="RelationQueryTitle"><FontAwesomeIcon icon={faBookOpen} /> <span>Detail Page</span></div>
      
      <div id='echartsRel' style={{ width: '600px', height: '400px', top:'20px', left:'300px' }}></div>
    </>
  )
}
