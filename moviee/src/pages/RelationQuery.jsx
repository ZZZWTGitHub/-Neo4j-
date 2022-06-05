import React from 'react'
import "./RelationQuery.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDiagramProject, faSearch } from "@fortawesome/free-solid-svg-icons";
import * as echarts from 'echarts'
import { useEffect } from 'react';

export default function RelationQuery() {

  useEffect(() => {
    //  模拟componentDidMount  首次渲染
    var myChart = echarts.init(document.getElementById('echartsRel'));

    myChart.setOption({
      title: {
        text: 'ECharts 例'
      },
      tooltip: {},
      xAxis: {
        data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
      },
      yAxis: {},
      series: [
        {
          name: '销量',
          type: 'bar',
          data: [5, 20, 36, 10, 10, 20]
        }
      ]
    });
  }, [])

  return (
    <>
      <div className="RelationQueryTitle"><FontAwesomeIcon icon={faDiagramProject} /> <span>Relation Query</span></div>
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
