const axios = require('axios');

const defaultState = {
  num: 100,
  entityQueryRes: [],
  detail: [
    "A League of Their Own",
    "Once in a lifetime you get a chance to do something different.",
    "1992"
  ],
};

// eslint-disable-next-line
export default (state = defaultState, action) => {
  let newState = JSON.parse(JSON.stringify(state));
  switch (action.type) {
    case "numAdd": {
      newState.num += action.value;
      break;
    }
    case "entityQuery": {
      const movieName = action.value;
      axios.get(`http://127.0.0.1:8000/movie?name=${movieName}`).then(res => {
        console.log(res, '++++');
        newState.entityQueryRes = res.data;
      }).catch(err => {
        console.log(err);
      });
      break;
    }
    case "queryDetail": {
      const movieName = action.value
      axios.get(`http://127.0.0.1:8000/moviedetail?movietitle=${movieName}`).then(res => {
        console.log(res, '++++');
        newState.detail = res.data;
      }).catch(err => {
        console.log(err);
      })
      break;
    };
    default: {
      console.log("no that action");
      break;
    }
  };
  return newState;
}