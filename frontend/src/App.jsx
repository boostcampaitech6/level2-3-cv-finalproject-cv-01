import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import ReactGA from 'react-ga4'; // GA4 버전을 사용한다고 가정
import { Loading } from "./screens/Loading";
import { Login } from "./screens/Login";
import { LoginKakao } from "./screens/LoginKakao";
import { SearchScreen } from "./screens/SearchScreen";
import { Home } from "./screens/Home";
import { Profile } from "./screens/Profile";
import { FavoriteScreen } from "./screens/FavoriteScreen";
import { ResultScreen } from "./screens/ResultScreen";
import { UserProvider } from "./components/UserContext";

// Google Analytics의 추적 ID
const TRACKING_ID = "G-8QXBPGZNVR";
ReactGA.initialize(TRACKING_ID);

// 사용자 정의 미들웨어를 통해 라우트 변경을 추적
const trackPageView = async (args) => {
  const location = args.location || args.router.location;
  const page = location.pathname + location.search;
  ReactGA.send({ hitType: "pageview", page: page });
};

const router = createBrowserRouter([
  {
    path: "/*",
    element: <Loading />,
  },
  {
    path: "/loading",
    element: <Loading />,
  },
  
  {
     // 라우터에 미들웨어 추가
    enhancers: [trackPageView],
  },
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/login-kakao",
    element: <LoginKakao />,
  },
  {
    path: "/search",
    element: <SearchScreen />,
  },
  {
    path: "/home",
    element: <Home />,
  },
  {
    path: "/profile",
    element: <Profile />,
  },
  {
    path: "/favorite",
    element: <FavoriteScreen />,
  },

  {
    path: "/result",
    element: <ResultScreen />,
  },

  {
    path: "/result/:symbol",
    element: <ResultScreen />,
  },
]);

export const App = () => {
  return (
    <UserProvider>
      <RouterProvider router={router} />;
    </UserProvider>
  )
};
