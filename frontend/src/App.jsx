import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Loading } from "./screens/Loading";
import { Element } from "./screens/Element";
import { Login } from "./screens/Login";
import { SearchScreen } from "./screens/SearchScreen";
import { LoginKakao } from "./screens/LoginKakao";
import { Home } from "./screens/Home";
import { DivWrapper } from "./screens/DivWrapper";
import { Profile } from "./screens/Profile";
import { Result } from "./screens/Result";
import { Favorite } from "./screens/Favorite";
import { Share } from "./screens/Share";
import { DivWrapperScreen } from "./screens/DivWrapperScreen";
import { LoginRequest } from "./screens/LoginRequest";
import { ResultScreen } from "./screens/ResultScreen";
import { Screen14 } from "./screens/Screen14";

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
    path: "/u35u4352u4455u4527u4352u4458-u4364u4453u4364u4449u4540u4370u4449u4352u4469u401u41",
    element: <Element />,
  },
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/search-2",
    element: <SearchScreen />,
  },
  {
    path: "/login-kakao",
    element: <LoginKakao />,
  },
  {
    path: "/home",
    element: <Home />,
  },
  {
    path: "/search-1",
    element: <DivWrapper />,
  },
  {
    path: "/profile",
    element: <Profile />,
  },
  {
    path: "/result-1",
    element: <Result />,
  },
  {
    path: "/favorite",
    element: <Favorite />,
  },
  {
    path: "/share",
    element: <Share />,
  },
  {
    path: "/u35u4367u4467u4527u4357u4469u4536u4359u4457u4355u4467",
    element: <DivWrapperScreen />,
  },
  {
    path: "/login-request",
    element: <LoginRequest />,
  },
  {
    path: "/result-2",
    element: <ResultScreen />,
  },
  {
    path: "/result-3",
    element: <Screen14 />,
  },
]);

export const App = () => {
  return <RouterProvider router={router} />;
};
