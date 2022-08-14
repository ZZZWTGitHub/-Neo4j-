import App from "../App";
import RelationQuery from "../pages/RelationQuery";
import Overview from "../pages/Overview";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Quest from "../pages/Quest";
import EntityQuery from "../pages/EntityQuery";
import Detail from "../pages/Detail";

const BaseRouter = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<App />}>
          <Route path='/entityquery' element={<EntityQuery />}></Route>
          <Route path='/relationquery' element={<RelationQuery />}></Route>
          <Route path='/overview' element={<Overview />}></Route>
          <Route path='/quest' element={<Quest />}></Route>
          <Route path='/detail' element={<Detail />}></Route>
        </Route>
      </Routes>
    </BrowserRouter>
  )
};

export default BaseRouter;