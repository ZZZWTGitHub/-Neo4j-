const defaultState = {
  num: 100
}

// eslint-disable-next-line
export default (state=defaultState, action) => {
  let newState = JSON.parse(JSON.stringify(state))
  switch(action.type){
    case "numAdd": {
      newState.num += action.value
      console.log(state.num)
      console.log(newState.num)
      console.log('++++++++')
      break
    }
    default: {
      console.log("no that action")
      break
    }
  }
  return newState
}