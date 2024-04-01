import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { DivWrapper } from "../../components/DivWrapper";
import { Menu } from "../../components/Menu";
import axios from 'axios';
import "./style.css";
import { useUser } from '../../components/UserContext'; // UserContext 사용
import { useNavigate } from "react-router-dom";

export const FavoriteScreen = () => {
  const KAKAO_AUTH_URL = `https://kauth.kakao.com/oauth/authorize?client_id=${process.env.REACT_APP_KAKAO_CLIENT_ID}&redirect_uri=${encodeURIComponent(process.env.REACT_APP_KAKAO_REDIRECT_URI)}&response_type=code`;

  const navigate = useNavigate(); // v6 사용 시

  const handleLogin = () => {
    navigate("/login"); // 로그인 페이지로 이동
  };

  const handleStockClick = (symbol, label, isFavorited) => {
    navigate(`/result/${symbol}`, { state: { stockLabel: label, isFavorited: isFavorited } });
  };

  const { userInfo } = useUser(); // UserContext로부터 사용자 정보를 가져옴
  const [favorites, setFavorites] = useState([]); // 즐겨찾기 목록 상태

  useEffect(() => {
    // 사용자가 로그인한 경우에만 즐겨찾기 정보를 불러옴
    if (userInfo) {
      const fetchFavorites = async () => {
        try {
          // 백엔드 API로부터 즐겨찾기 목록을 불러옴
          const response = await axios.get(`http://${process.env.SERVER_IP}:8001/user/favorite/${userInfo.kakao_id}`);
          const favoriteStocks = response.data; // 응답 데이터

          const stockDetails = await Promise.all(favoriteStocks.map(async (stock) => {
            // 각 즐겨찾기 주식의 상세 정보를 불러옴
            const symbol = stock.stock_code.slice(-6);
            const detailResponse = await axios.get(`http://${process.env.SERVER_IP}:8001/api/stock/${symbol}`);
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
          {userInfo ? (
            <>
              <div className="button-3">
                <Link to="/search"><img className="img-2" alt="Plus" src="/img/plus.svg" /></Link>
              </div>
            <div className="favorite-list-container">
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
                    onClick={() => handleStockClick(favorite.symbol, favorite.stock_name, favorite.isFavorited)} // Add this line
                />

                )) : (
                  <div className="text-container">
                    <div className="text">
                  <p className='text-style'>즐겨찾기 목록이 비어 있습니다.</p>
                  </div>
                  </div>
                )}
              </div>
              </div>
            </>
          ) : (
            <div className="favorite-list">
              <div className="text-container-2">
                    <div className="text">
                  <p className='text-style'>즐겨찾기를 보려면 로그인해주세요.</p>
                  </div>
                  <a href={KAKAO_AUTH_URL} className="button-kakao-login">
                  <button  onClick={handleLogin}   className="button-2">
              <img className="kakao-logo" alt="Kakao logo" src="/img/kakao-logo.svg" />
              <div className="label-wrapper">
                <div className="label">카카오 로그인</div>
              </div>
            </button>
            </a>
                  </div>
            </div>
          )}

         <div className="line">
                  <img className="line-2" alt="Line" src="/img/line-2.svg" />
                </div>
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
  );
};
