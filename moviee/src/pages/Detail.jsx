import React from 'react'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBookOpen } from "@fortawesome/free-solid-svg-icons";
// import { useSearchParams } from "react-router-dom"; 
import { connect } from "react-redux"
// import { useEffect } from 'react';

function Detail(props) {
  // eslint-disable-next-line
  // const [searchParams, setSearchParams] = useSearchParams()
  // const useID = searchParams.get('movietitle')

  // useEffect(() => {
  //   props.queryDetail(useID)
  // }, [])
  
  return (
    <>
      <div className="RelationQueryTitle"><FontAwesomeIcon icon={faBookOpen} /> <span>Detail Page</span></div>
      
    </>
  )
}

const mapStateToProps = (state) => {
  return {
    detail: state.detail
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    queryDetail(movietitle) {
      const action = { type: 'queryDetail', value: movietitle }
      dispatch(action)
    }
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Detail)