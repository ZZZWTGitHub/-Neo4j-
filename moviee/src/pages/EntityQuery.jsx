import React from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import "./EntityQuery.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import axios from 'axios'
import { connect } from "react-redux";

function EntityQuery(props) {
  // eslint-disable-next-line
  const [searchParams, setSearchParams] = useSearchParams()
  // console.log(searchParams.get('id'))
  const useID = searchParams.get('id')

  const navigate = useNavigate()

  const goDetail = (title) => {
    navigate('/detail?movietitle=' + title)
  }

  var timeOut = null

  const antiShake = (fn, wait) => {
    return args => {
      if (timeOut) {
        clearTimeout(timeOut)
      }
      // 如果有timeOut，清除并重新请求
      fn()
      timeOut = setTimeout(fn, wait)
    }
  }

  const searchMovie = () => props.entityQuery(document.getElementsByClassName('search-input')[0].value)
  

  return (
    <>
      <div className="EntityQueryTitle"><FontAwesomeIcon icon={faSearch} /> <span>Entity Query</span></div>
      {/* <h2>Home of {useID}</h2> */}
      <div className="search">
        <div className="search-box">
          <input type="text"
            className="search-input"
            placeholder="Input the Entity you want to search..."
            onKeyDown={antiShake(searchMovie, 2000)} />
          <button type="submit"
            className="search-btn"
            onClick={antiShake(searchMovie, 2000)}>
            <FontAwesomeIcon icon={faSearch} />
          </button>
        </div>
      </div>
      <div className="EntityResults">
        {
          props.entityQueryRes.map((name, index) => {
            return (
              <div className="Entity" key={name[0]} onClick={() => { goDetail(name[0]) }}>
                <h3 className="EntityName">{name[0]}</h3>
                <p className="EntityDetail">{name[1]}</p>
              </div>
            )
          })
        }
      </div>
    </>
  )
}

const mapStateToProps = (state) => {
  return {
    entityQueryRes: state.entityQueryRes
  }
}

// 事件派发映射：将reducer中事件映射到props，以便组件使用其中的方法
const mapDispatchToProps = (dispatch) => {
  return {
    entityQuery(movieName) {
      const action = { type: 'entityQuery', value: movieName }
      dispatch(action)
    }
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(EntityQuery)