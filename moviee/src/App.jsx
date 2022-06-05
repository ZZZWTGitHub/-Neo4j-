import React, { Fragment } from 'react'
import { connect } from 'react-redux'
import { Outlet, useLocation, useNavigate } from 'react-router-dom'
import logo from "./image/logo_moviee.png"

import "./App.css"

function App(props) {

  const logoURL = logo

  const location = useLocation()
  const navigate = useNavigate()
  // console.log(location.pathname)

  const goHome = () => {
    navigate('/entityquery')
  }

  const goList = () => {
    navigate('/relationquery')
  }

  const goOverview = () => {
    navigate('/overview')
  }

  const goQuest = () => {
    navigate('/quest')
  }

  return (
    <Fragment>
      <div className='appPage'>
        <div className='header'>
          <img src={logoURL} alt="" height={150} />
        </div>
        <div className='container'>
          <div className='aside'>
            <button onClick={goHome} className={location.pathname === '/entityquery' ? 'active' : ''}>Entity Query</button>
            <button onClick={goList} className={location.pathname === '/relationquery' ? 'active' : ''}>Relation Query</button>
            <button onClick={goOverview} className={location.pathname === '/overview' ? 'active' : ''}>Graph Overview</button>
            <button onClick={goQuest} className={location.pathname === '/quest' ? 'active' : ''}>Intelligent Q&#38;A</button>
          </div>
          <div className='mainbox'><Outlet /></div>
        </div>
      </div>
      {/* <hr />
      <h2>Test of React redux</h2>
      <p>num store in redux: {props.num}</p>
      <button onClick={() => props.numAdd()}>add</button>
      <hr />
      <h2>Test of React router</h2>
      <ul>
        <li><Link to="/home?id=admin">home</Link></li>
        <li><Link to="/list">list</Link></li>
        <li><Link to="detail/123456">detail</Link></li>
      </ul>
      <hr />
      <button onClick={goHome}>HOME</button>
      <button onClick={goList}>LIST</button>
      <button onClick={goDetail}>DETAIL</button>
      <hr /> */}
      {/* <Outlet /> */}
      {/* render child router element here */}
    </Fragment>
  )
}

// 状态映射：reducer中的state，映射到props，以便调用state中的数据
const mapStateToProps = (state) => {
  return {
    num: state.num
  }
}

// 事件派发映射：将reducer中事件映射到props，以便组件使用其中的方法
const mapDispatchToProps = (dispatch) => {
  return {
    numAdd() {
      const action = { type: 'numAdd', value: 2 }
      dispatch(action)
    }
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(App)