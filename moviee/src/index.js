import ReactDOM from "react-dom";
// import App from "./App";
// test of redux
import { Provider } from "react-redux";
import store from "./store";
// test of router
import Router from './router/index';
// clear origin style
import "./reset.css";


ReactDOM.render(
  <Provider store={store}>
    <Router />
  </Provider>,
  document.getElementById('root')
);