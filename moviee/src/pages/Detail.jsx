import React from 'react'
import { useSearchParams } from 'react-router-dom'
import * as echarts from 'echarts'
import { useEffect } from 'react'

export default function Detail() {
  // eslint-disable-next-line
  const [searchParams, setSearchParams] = useSearchParams()
  const thingToSearch = searchParams.get('thing')
  console.log(echarts.init)

  useEffect(() => {
    //  模拟componentDidMount  首次渲染
    var myChart = echarts.init(document.getElementById('echartsAll'));

    myChart.setOption({
      title: {
        text: 'ECharts 入门示例'
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
      {/* <h2>Detail</h2>
      <p>thingToSearch is {thingToSearch}</p> */}
      <div id='echartsAll' style={{ width: '600px', height: '400px', top:'100px', left:'300px' }}></div>

    </>
  )
}
