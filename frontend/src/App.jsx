import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Loading } from "./screens/Loading";
import { Share } from "./screens/Share";
import { Login } from "./screens/Login";
import { LoginKakao } from "./screens/LoginKakao";
import { SearchScreen } from "./screens/SearchScreen";
import { Home } from "./screens/Home";
import { Profile } from "./screens/Profile";
import { FavoriteScreen } from "./screens/FavoriteScreen";
import { Result } from "./screens/Result";
import { ResultScreen } from "./screens/ResultScreen";
import { ResultWrapper } from "./screens/ResultWrapper";
import { FavoriteWrapper } from "./screens/FavoriteWrapper";
import { UserProvider } from "./components/UserContext";

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
    path: "/share",
    element: <Share />,
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
    path: "/result-3",
    element: <Result />,
  },
  {
    path: "/result",
    element: <ResultScreen />,
  },
  {
    path: "/result-2",
    element: <ResultWrapper />,
  },
  {
    path: "/favorite-2",
    element: <FavoriteWrapper />,
  },
]);

export const App = () => {
  return (
    <UserProvider>
      <RouterProvider router={router} />;
    </UserProvider>
  )
};
