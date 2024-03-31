import React from 'react';
import { useNavigate } from 'react-router-dom';
import introVideoDesktop from "../../../dist/video/intro_desktop.mp4";
import introVideoMobile from "../../../dist/video/intro_mobile.mp4";
import "./style.css";

export const Loading = () => {
  const navigate = useNavigate();

  const handleVideoEnd = () => {
    setTimeout(() => {
      navigate('/login');
    }, 800);
  };

  return (
    <div className="video-container">
      <video autoPlay muted className="video desktop-video" onEnded={handleVideoEnd}>
        <source src={introVideoDesktop} type="video/mp4" />
      </video>
      <video autoPlay muted className="video mobile-video" onEnded={handleVideoEnd}>
        <source src={introVideoMobile} type="video/mp4" />
      </video>
    </div>
  );
};