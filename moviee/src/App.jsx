import React, {Fragment} from 'react'
import { connect } from 'react-redux'
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom'

function App(props) {
  const location = useLocation()
  const navigate = useNavigate()
  console.log(location.pathname)

  const goHome = () => {
    navigate('/home?id=zzzwt')
  }

  const goList = () => {
    navigate('/list')
  }

  const goDetail = () => {
    navigate('/detail/456789')
  }

  return (
    <Fragment>
      <div>App</div>
      <hr />
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
      <hr />
      <Outlet />
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
      const action = {type: 'numAdd', value: 2}
      dispatch(action)
    }
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(App)