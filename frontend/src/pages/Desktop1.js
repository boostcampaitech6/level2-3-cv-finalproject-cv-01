import React, { useState, useEffect, FunctionComponent, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./Desktop1.module.css";
import { AdvancedRealTimeChart } from "react-ts-tradingview-widgets";
import AsyncSelect from 'react-select/async';
import Papa from 'papaparse';

const Desktop1 = () => {
  const navigate = useNavigate();

  const onAITextClick = useCallback(() => {
    navigate("/");
  }, [navigate]);

  const onLinkContainerClick = useCallback(() => {
    window.open("https://www.yna.co.kr/view/AKR20240304144500017");
  }, []);

  const onLinkContainer2Click = useCallback(() => {
    window.open("https://www.yna.co.kr/view/AKR20240304144500017");
  }, []);

  const onLinkContainer3Click = useCallback(() => {
    window.open("http://www.newsis.com/view/");
  }, []);

  const onLinkContainer4Click = useCallback(() => {
    window.open("http://www.newsis.com/view/");
  }, []);

  const onLinkContainer5Click = useCallback(() => {
    window.open("https://www.busan.com/view/busan/view.php");
  }, []);

  const onLinkContainer6Click = useCallback(() => {
    window.open("https://www.busan.com/view/busan/view.php");
  }, []);

  const onLinkContainer7Click = useCallback(() => {
    window.open("http://news.heraldcorp.com/view.php");
  }, []);

  const onLinkContainer8Click = useCallback(() => {
    window.open("http://news.heraldcorp.com/view.php");
  }, []);

  const [stocksData, setStocksData] = useState([]);
  const [selectedSymbol, setSelectedSymbol] = useState(null);

  useEffect(() => {
    Papa.parse('/symbol_data/korea_stock_symbols.csv', {
      download: true,
      header: true,
      complete: function(results) {
        setStocksData(results.data);
      },
    });
  }, []);

  // 자동완성 옵션 로드 함수
  const loadOptions = (inputValue, callback) => {
    setTimeout(() => {
      // 검색어가 비어 있지 않은 경우에만 필터링 수행
      if (inputValue.trim() !== "") {
        const filteredOptions = stocksData.filter((stock) =>
        stock.label && stock.label.toLowerCase().includes(inputValue.toLowerCase())
        );
        callback(filteredOptions);
      } else {
        // 검색어가 비어 있는 경우 전체 목록 반환 또는 빈 배열 반환
        callback([]);
      }
    }, 500); // 예시로 1초 딜레이를 줍니다 (실제 사용 시 조정 가능)
  };

  // 선택된 옵션을 처리하는 함수
  const handleChange = (selectedOption) => {
    if (selectedOption) {
      setSelectedSymbol(selectedOption.value);
    } else {
      setSelectedSymbol(null);
    }
  };

  return (
    <div className={styles.desktop2}>
      <div className={styles.ai} onClick={onAITextClick}>
        <span>알려</span>
        <span className={styles.span}>주가</span>
        <span className={styles.ai1}>AI</span>
      </div>
      <div className={styles.market}>Market</div>
      <div className={styles.prediction}>Prediction</div>
      <div className={styles.game}>Game</div>
      <div className={styles.aboutUs}>About us</div>
      <div className={styles.login}>Login</div>
      <img className={styles.coinIcon} alt="" src="/coin.svg" />

      <div className={styles.searchBar}>
        <AsyncSelect
          cacheOptions
          placeholder='주식 종목명을 입력해주세요.'
          loadOptions={loadOptions}
          defaultOptions
          onChange={handleChange}
          getOptionLabel={(e) => e.label}
          getOptionValue={(e) => e.value}
          isClearable
          className={styles.searchInput} // 이 클래스는 실제로는 적용되지 않습니다.
          styles={{
            container: (provided) => ({
              ...provided,
              width: '100%', // 컨테이너의 너비를 100%로 설정
            }),
            control: (provided) => ({
              ...provided,
              width: '100%', // 검색창 컨트롤의 너비를 100%로 설정
            }),
            option: (provided) => ({
              ...provided,
              color: 'black', // 옵션의 글씨 색깔을 검은색으로 설정
            }),
          }}
        />
        {selectedSymbol && <AdvancedRealTimeChart symbol={selectedSymbol} theme="dark"/>}
      </div>

      <div className={styles.itemParent}>
        <div className={styles.item}>
          <div className={styles.divtext}>
            <div className={styles.link} onClick={onLinkContainerClick}>
              <div className={styles.heading3}>
                <div className={styles.div}>
                  네이버 카페, 호주·뉴질랜드서 6일간 접속 오류
                </div>
              </div>
              <a
                className={styles.a}
                href="https://www.yna.co.kr/view/AKR20240304144500017"
                target="_blank"
              >
                9시간 전
              </a>
            </div>
            <div className={styles.divactionButtons}>
              <div className={styles.button}>
                <div className={styles.div1}>부정</div>
              </div>
            </div>
          </div>
          <div className={styles.divimagemargin}>
            <div className={styles.divimage}>
              <div className={styles.link1} onClick={onLinkContainer2Click}>
                <img
                  className={styles.newsDefault5webpIcon}
                  alt=""
                  src="/newsdefault5webp@2x.png"
                />
              </div>
            </div>
          </div>
        </div>
        <div className={styles.item1}>
          <div className={styles.divtext1}>
            <div className={styles.link2} onClick={onLinkContainer3Click}>
              <div className={styles.heading31}>
                <div className={styles.div}>
                  <p className={styles.p}>
                    카드사 네이버 포인트 누락에…금감원 "상반기 중 환급해야"</p>
                </div>
              </div>
              <div className={styles.divsubText}>
                <a
                  className={styles.a1}
                  href="http://www.newsis.com/view/"
                  target="_blank"
                >
                  뉴시스
                </a>
                <a
                  className={styles.a1}
                  href="http://www.newsis.com/view/"
                  target="_blank"
                >
                  |
                </a>
                <a
                  className={styles.a1}
                  href="http://www.newsis.com/view/"
                  target="_blank"
                >
                  16시간 전
                </a>
              </div>
            </div>
            <div className={styles.divactionButtons}>
              <div className={styles.button}>
                <div className={styles.div1}>부정</div>
              </div>
            </div>
          </div>
          <div className={styles.divimagemargin1}>
            <div className={styles.divimage1}>
              <div className={styles.link1} onClick={onLinkContainer4Click}>
                <img
                  className={styles.newsDefault5webpIcon}
                  alt=""
                  src="/nisi20210205-0000686568-webjpg@2x.png"
                />
              </div>
            </div>
          </div>
        </div>
        <div className={styles.item2}>
          <div className={styles.divtext2}>
            <div className={styles.link2} onClick={onLinkContainer5Click}>
              <div className={styles.heading32}>
                <div className={styles.div}>
                  <p className={styles.p}>
                    금감원, 네이버포인트 누락 현대카드 등에 ‘환급’ 지시</p>
                </div>
              </div>
              <div className={styles.divsubText1}>
                <a
                  className={styles.a1}
                  href="https://www.busan.com/view/busan/view.php"
                  target="_blank"
                >
                  부산일보
                </a>
                <a
                  className={styles.a1}
                  href="https://www.busan.com/view/busan/view.php"
                  target="_blank"
                >
                  |
                </a>
                <a
                  className={styles.a1}
                  href="https://www.busan.com/view/busan/view.php"
                  target="_blank"
                >
                  17시간 전
                </a>
              </div>
            </div>
            <div className={styles.divactionButtons}>
              <div className={styles.button}>
                <div className={styles.div1}>부정</div>
              </div>
            </div>
          </div>
          <div className={styles.divimagemargin1}>
            <div className={styles.divimage2}>
              <div className={styles.link5} onClick={onLinkContainer6Click}>
                <img
                  className={styles.newsDefault5webpIcon}
                  alt=""
                  src="/newsdefault2webp@2x.png"
                />
              </div>
            </div>
          </div>
        </div>
        <div className={styles.item3}>
          <div className={styles.divtext1}>
            <div className={styles.link2} onClick={onLinkContainer7Click}>
              <div className={styles.heading33}>
                <div className={styles.div}>
                  <p className={styles.p}>
                    ‘네이버 포인트’ 누락한 카드사…금감원 “상반기까지 환급해야”</p>
                </div>
              </div>
              <div className={styles.divsubText2}>
                <a
                  className={styles.a1}
                  href="http://news.heraldcorp.com/view.php"
                  target="_blank"
                >
                  헤럴드경제
                </a>
                <a
                  className={styles.a1}
                  href="http://news.heraldcorp.com/view.php"
                  target="_blank"
                >
                  |
                </a>
                <a
                  className={styles.a1}
                  href="http://news.heraldcorp.com/view.php"
                  target="_blank"
                >
                  19시간 전
                </a>
              </div>
            </div>
            <div className={styles.divactionButtons}>
              <div className={styles.button}>
                <div className={styles.div1}>부정</div>
              </div>
            </div>
          </div>
          <div className={styles.divimagemargin1}>
            <div className={styles.divimage1}>
              <div className={styles.link1} onClick={onLinkContainer8Click}>
                <img
                  className={styles.newsDefault5webpIcon}
                  alt=""
                  src="/20240304050098-pjpg@2x.png"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* <div className={styles.parent}>
        <div className={styles.div8}>관심종목</div>
        <div className={styles.rectangleParent}>
          <div className={styles.frameChild} />
          <img className={styles.arrowDownIcon} alt="" src="/arrow-down.svg" />
        </div>
        <div className={styles.rectangleWrapper}>
          <div className={styles.frameItem} />
        </div>
        <div className={styles.div9}>네이버</div>
        <img className={styles.frameInner} alt="" src="/vector-3.svg" />
        <img className={styles.vectorIcon} alt="" src="/vector.svg" />
      </div> */}
      <div className={styles.image7Parent}>
        <img className={styles.image7Icon} alt="" src="/image-7@2x.png" />
        <div className={styles.aiContainer}>
          <p className={styles.p}>알려주가AI가 네이버 주가를 분석한 결과</p>
          <p className={styles.p}>{`오늘인 2024년 3월 4일 기준으로 `}</p>
          <p className={styles.p}>5일 이후인 2024년 03월 09일에는</p>
          <p className={styles.p}>
            <span>{`56.41% 확신으로 `}</span>
            <span className={styles.span1}>상승</span>
            <span>을</span>
          </p>
          <p className={styles.p}>20일 이후인 2024년 03월 24일에는</p>
          <p className={styles.p}>
            <span>{`66.96% 확신으로 `}</span>
            <span className={styles.span1}>상승</span>
            <span className={styles.span3}>을 예측했어요!</span>
          </p>
        </div>
      </div>
      {/* <img className={styles.image8Icon} alt="" src="/image-8@2x.png" /> */}
    </div>
  );
};

export default Desktop1;
