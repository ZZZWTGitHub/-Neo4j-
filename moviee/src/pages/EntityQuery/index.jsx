import React from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import "./EntityQuery.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
// import axios from 'axios';
import { connect } from "react-redux";
// import { useEffect } from "react";

function EntityQuery(props) {
  // eslint-disable-next-line
  const [searchParams, setSearchParams] = useSearchParams();
  // console.log(searchParams.get('id'))
  // const useID = searchParams.get('id');

  const navigate = useNavigate();

  const goDetail = (title) => {
    navigate('/detail?movietitle=' + title);
  }

  const antiShake = (fn, wait) => {
    var timeOut = null;
    return args => {
      if (timeOut) {
        clearTimeout(timeOut);
      };
      // 如果有timeOut，清除并重新请求
      timeOut = setTimeout(fn, wait);
    }
  }

  // useEffect(() => {
  //   console.log(999999999, props);
  // })

  const searchMovie = () => {
    // const res = props.entityQuery(document.getElementsByClassName('search-input')[0].value);
    console.log(111111, props, document.getElementsByClassName('search-input')[0].value);
    // return res;
    props.entityQuery(document.getElementsByClassName('search-input')[0].value);
  }

  return (
    <>
      <div className="EntityQueryTitle"><FontAwesomeIcon icon={faSearch} /> <span>Entity Query</span></div>
      {/* <h2>Home of {useID}</h2> */}
      <div className="search">
        <div className="search-box">
          <input type="text"
            className="search-input"
            placeholder="Input the Entity you want to search..."
            onKeyDown={antiShake(searchMovie, 30)} />
          <button type="submit"
            className="search-btn"
            onClick={antiShake(searchMovie, 30)}>
            <FontAwesomeIcon icon={faSearch} />
          </button>
        </div>
      </div>
      <div className="EntityResults">
        {
          props.entityQueryRes &&
          props.entityQueryRes.map((item, index) => {
            return (
              <div className="Entity" key={item.movie_name} onClick={() => { goDetail(item.movie_name) }}>
                <h3 className="EntityName">{item.movie_name}</h3>
                <p className="EntityDetail">{item.year}</p>
              </div>
            )
          })
        }
      </div>
    </>
  );
}

const mapStateToProps = (state) => {
  return {
    entityQueryRes: state.entityQueryRes || []
  };
};

// 事件派发映射：将reducer中事件映射到props，以便组件使用其中的方法
const mapDispatchToProps = (dispatch) => {
  return {
    entityQuery(movieName) {
      const action = { type: 'entityQuery', value: movieName };
      dispatch(action);
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(EntityQuery);