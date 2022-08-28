import React from 'react';
import "../RelationQuery/RelationQuery.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch, faComment } from "@fortawesome/free-solid-svg-icons";
import { useSearchParams, useNavigate } from "react-router-dom";
import { connect } from "react-redux";
// import { faC } from '@fortawesome/free-solid-svg-icons';
// import * as echarts from 'echarts';
import { useEffect } from 'react';

function Quest(props) {
  // eslint-disable-next-line
  const [searchParams, setSearchParams] = useSearchParams();

  const navigate = useNavigate();

  const goDetail = (title) => {
    navigate('/detail?movietitle=' + title);
  }

  const antiShake = (fn, wait) => {
    var timeOut = null;
    return () => {
      if (timeOut) {
        clearTimeout(timeOut);
      };
      // 如果有timeOut，清除并重新请求
      timeOut = setTimeout(fn, wait);
    }
  }

  const questMovie = () => {
    console.log(111111, props, document.getElementsByClassName('search-input')[0].value);
    // return res;
    props.quest(document.getElementsByClassName('search-input')[0].value);
  }

  useEffect(() => {
    console.log(999999999, props);
  })

  return (
    <>
      <div className="RelationQueryTitle"><FontAwesomeIcon icon={faComment} /> <span>Intelligent Q&#38;A</span></div>
      <div className="search">
        <div className="search-box">
          <input type="text"
            className="search-input"
            placeholder="Input the Entity you want to search..."
            onKeyDown={antiShake(questMovie, 300)} 
          />
          <button type="submit"
            className="search-btn"
            onClick={antiShake(questMovie, 300)}>
            <FontAwesomeIcon icon={faSearch} />
          </button>  
        </div>
      </div>
      <div className="EntityResults">
        {
          props.questRes &&
          (
            <div className="Entity" key={props.questRes} onClick={() => { goDetail(props.questRes) }}>
              <h3 className="EntityName">{props.questRes}</h3>
              <p className="EntityDetail">{props.questRes}</p>
            </div>
          )
        }
      </div>
    </>
  );
};

const mapStateToProps = (state) => {
  return {
    questRes: state.questRes || ''
  };
};

// 事件派发映射：将reducer中事件映射到props，以便组件使用其中的方法
const mapDispatchToProps = (dispatch) => {
  return {
    quest(movieName) {
      const action = { type: 'quest', value: movieName };
      console.log('action.value: ', action.value)
      dispatch(action);
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Quest);