import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { DivWrapper } from "../../components/DivWrapper";
import { Menu } from "../../components/Menu";
import axios from 'axios';
import "./style.css";
import { useUser } from '../../components/UserContext'; // UserContext 사용
import { useNavigate } from "react-router-dom";

export const FavoriteScreen = () => {
  const navigate = useNavigate(); // v6 사용 시

  const handleLogin = () => {
    navigate("/login"); // 로그인 페이지로 이동
  };

  const { userInfo } = useUser(); // UserContext로부터 사용자 정보를 가져옴
  const [favorites, setFavorites] = useState([]); // 즐겨찾기 목록 상태

  useEffect(() => {
    // 사용자가 로그인한 경우에만 즐겨찾기 정보를 불러옴
    if (userInfo) {
      const fetchFavorites = async () => {
        try {
          // 백엔드 API로부터 즐겨찾기 목록을 불러옴
          const response = await axios.get(`http://localhost:8000/user/favorite/${userInfo.kakao_id}`);
          const favoriteStocks = response.data; // 응답 데이터

          const stockDetails = await Promise.all(favoriteStocks.map(async (stock) => {
            // 각 즐겨찾기 주식의 상세 정보를 불러옴
            const symbol = stock.stock_code.slice(-6);
            const detailResponse = await axios.get(`http://localhost:8000/api/stock/${symbol}`);
            return { ...detailResponse.data,
              change: (detailResponse.data.change * 100).toFixed(2)
            };
          }));
          console.log(stockDetails)
          setFavorites(stockDetails);
        } catch (error) {
          console.error("Error fetching favorites:", error);
          setFavorites([]);
        }
      };

      fetchFavorites();
    }
  }, [userInfo]); // user가 변경될 때마다 이 useEffect가 실행됨

  return (
    <div className="favorite-screen">
      <div className="frame-10">
        <div className="content-6">
          {userInfo ? (
            <>
              <div className="button-3">
                <Link to="/search"><img className="img-2" alt="Plus" src="/img/plus.svg" /></Link>
              </div>
              <div className="favorite-list">
                {favorites.length > 0 ? favorites.map((favorite, index) => (
                  <DivWrapper
                    key={index}
                    className="component-1175"
                    companyName={favorite.stock_name}
                    symbol={favorite.symbol}
                    price={`${favorite.close}원`}
                    change={`Change: ${favorite.change} %`}
                    volume={`Volume: ${favorite.volume}`}
                    graph="/img/frame-40.svg"
                    logo={favorite.logo}
                />
                )) : (
                  <p>즐겨찾기 목록이 비어 있습니다.</p>
                )}
              </div>
            </>
          ) : (
            <div className="favorite-list">
              <p>즐겨찾기를 보려면 로그인해주세요.</p>
              <button onClick={handleLogin} className="login-button">로그인</button>
            </div>
          )}
          <div className="menu-bar-2">
            <Menu
              className="menu-4"
              iconVariantsIconHome="/img/home-7.svg"
              iconVariantsIconUnion="/img/union-9.svg"
              iconVariantsIconUser="/img/user.svg"
              iconVariantsState="off"
              iconVariantsState1="off"
              iconVariantsState2="off"
              iconVariantsState3="on"
              to="/home"
              to2="/profile"
              to3="/search"
            />
          </div>
          <div className="head-4">
            <div className="text-wrapper-33">Favorite</div>
          </div>
        </div>
      </div>
    </div>
  );
};
