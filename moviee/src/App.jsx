import React, {Fragment} from 'react'
import { connect } from 'react-redux'

function App(props) {
  return (
    <Fragment>
      <div>App</div>
      <hr />
      <h2>Test of React redux</h2>
      <p>num store in redux: {props.num}</p>
      <button onClick={() => props.numAdd()}>add</button>
      <hr />
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