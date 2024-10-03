import React from 'react';
import ReactPlayer from 'react-player';
import { useScrollReveal } from '.';


const VideoPlayer = () => {
  useScrollReveal();
  return (
    <div className='slide-up flex flex-col  items-center  '>
      
      <h1 className="text-[2rem] padding-t text-center text-[#67754a] ">
      Introduction to Greenhouse Gases: What You Need to Know!
      </h1>
      <p className="p-5 w-4/5 text-center">
      Welcome to the Greenhouse Effect Fun Zone!  Here, you’ll find awesome videos that explain the greenhouse effect in a snap, and some cool comics made with Phaser that dive into the world of greenhouse gases!
      Greenhouse gases keep our planet nice and toasty, like a warm blanket! But watch out—the greenhouse effect can turn that cozy vibe into a wild heatwave, causing chaos in our climate!  Let’s learn how to keep things comfy without turning up the heat, play the animation video below!
        </p>
    <div className="flex justify-center items-center p-2 mb-[2rem]">
      <ReactPlayer
        url="/video/animaker.mp4"
        controls
        className="rounded-lg shadow-lg"
      />
    </div>
    </div>
  );
};

export default VideoPlayer;
