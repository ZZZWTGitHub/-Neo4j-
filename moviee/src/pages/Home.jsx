import React from "react";
import { useSearchParams } from "react-router-dom";
import "./Home.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";

export default function Home() {
  // eslint-disable-next-line
  const [searchParams, setSearchParams] = useSearchParams()
  // console.log(searchParams.get('id'))
  const useID = searchParams.get('id')
  return (
    <>
      <div className="EntityQueryTitle"><FontAwesomeIcon icon={faSearch} /> <span>Entity Query</span></div>
      {/* <h2>Home of {useID}</h2> */}
      <div className="search">
        <div className="search-box">
          <input type="text" className="search-input" placeholder="Input the Entity you want to search..." />
          <button type="submit" className="search-btn"><FontAwesomeIcon icon={faSearch} /></button>
        </div>
      </div>
      <div className="EntityResults">
        <div className="Entity">
          <h3 className="EntityName">斯坦利·库布里克</h3>
          <p className="EntityDetail">这里是一段详细的介绍...斯坦利·库布里克是过去40年间始终最吸引人的电影制作人 他的作品受到的赞扬几乎和招致的咒骂一样多。影片中不可思议的视觉风格为他赢得如潮好评，而他非传统的叙述感又常常会引来轻蔑的挑剔。尽管如此，他在重复和模仿主导的传媒圈仍旧是一位独一无二的艺术家。</p>
        </div>
        <div className="Entity">
          <h3 className="EntityName">斯坦利·库布里克</h3>
          <p className="EntityDetail">这里是一段详细的介绍...斯坦利·库布里克是过去40年间始终最吸引人的电影制作人 他的作品受到的赞扬几乎和招致的咒骂一样多。影片中不可思议的视觉风格为他赢得如潮好评，而他非传统的叙述感又常常会引来轻蔑的挑剔。尽管如此，他在重复和模仿主导的传媒圈仍旧是一位独一无二的艺术家。</p>
        </div>
      </div>
    </>
  )
}
