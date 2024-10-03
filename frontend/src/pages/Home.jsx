import { rand_pics } from "@/assets/constants";
import Hero from "@/components/Hero";
import MultipleSlides from "@/components/MultipleSlides";
import React, { useEffect } from "react";
import { g1 } from "@/assets/images";
import { Button, GameButton, useScrollReveal } from "@/components";
import "../style/font.css";
import ScrollReveal from "scrollreveal";


const Home = () => {
  useScrollReveal();

  return (
    <div style={{
      backgroundImage: `url('p1 (2).jpg')`, // Replace with your image path
      backgroundPosition: "center",
        backgroundAttachment: "fixed",
        backgroundRepeat: "no-repeat",
        backgroundSize: "cover", // Optional: set height as per your design
    }}>
      {/* Apply animation to the Hero section */}
      <div className="slide-left">
        <Hero />
      </div>

      <div className="max-container w-4/5 mx-auto">
        <hr className="my-4 h-[2px] bg-[#e3dddd] border-0" />
      </div>

      <div className="slide-left">
        <div>
          <h1 className="flex mb-5 text-col xl:flex-row flex-col justify-center items-center font-palanquin lg:text-3xl sm:text-xl lg:leading-[30px] xl:leading-[40px] lg:pt-10 z-10 sm:pt-20 font-bold text-col slow-fade-in title-bold">
            Explore the World of Greenhouse Gases
          </h1>
          <div
  className="container"
  style={{
    width: "100%",
    height: "auto", // Changed to auto
    margin: "0 !important",
    display: "flex", // Optional: Ensure flex layout if needed
    flexWrap: "wrap", // Optional: Allow wrapping if needed
  }}
>
  <div className="row col-p-0 font-mono" style={{ width: "100%" }}>
    <div className="col-sm-4 col-p-0" style={{ position: "relative" }}>
      <img src="ogrobot.jpg" alt="" />
      <div style={{ position: "absolute", top: "30px", left: "30px" }}>
        <button className="btn btn-info">
          {" "}
          <a href="/ogrobot">Chat With Ogrobot</a>
        </button>
      </div>
      <div
        className="text-white "
        style={{
          position: "absolute",
          bottom: "0px",
          left: "0px",
          padding: "20px",
          backgroundImage: "linear-gradient(to top, black , transparent)",
        }}
      >
        Want to know more about how you can contribute to reduce greenhouse gas emission? Ogrobot is here to talk with you!
      </div>
    </div>
    <div className="col-sm-4 col-p-0" style={{ position: "relative" }}>
      <img src="learn_ghg.jpg" alt="" />
      <div style={{ position: "absolute", top: "30px", left: "30px" }}>
        <button className="btn btn-warning">
          {" "}
          <a href="/education">Learn about Green House Gas</a>
        </button>
      </div>
      <div
        className="text-white"
        style={{
          position: "absolute",
          bottom: "0px",
          left: "0px",
          padding: "20px",
          backgroundImage: "linear-gradient(to top, black , transparent)",
        }}
      >
        Let's dive into learning more about greenhouse gas through interactive learning like comics, video tutorials, and many more!
      </div>
    </div>
    <div className="col-sm-4 col-p-0" style={{ position: "relative" }}>
      <img src="quiz.jpg" alt="" />
      <div style={{ position: "absolute", top: "30px", left: "30px" }}>
        <button className="btn btn-info">
          {" "}
          <a href="/game">Play Quiz</a>
        </button>
      </div>
      <div
        className="text-white"
        style={{
          position: "absolute",
          bottom: "0px",
          left: "0px",
          padding: "20px",
          backgroundImage: "linear-gradient(to top, black , transparent)",
        }}
      >
        Ok, now let's test our learning through an interactive quiz game! Ready to earn some points? Lets get started.
      </div>
    </div>
  </div>
</div>


            <div className="max-container w-4/5 mx-auto">
              <hr className="my-4 h-[2px] bg-[#e3dddd] border-0" />
            </div>
            <div className="">
        <div className="max-container w-4/5 mx-auto ">
          <h1 className="flex xl:flex-row text-col flex-col text-col justify-center items-center font-palanquin lg:text-3xl sm:text-xl lg:leading-[30px] xl:leading-[40px] lg:pt-10 z-10 sm:pt-20 font-bold slow-fade-in">
            Explore Map
          </h1>
        </div>

        <div className="flex items-center justify-center text-center">
          <p className="w-4/5 font-montserrat text-slate-gray text-lg mt-6 mb-[1rem] sm-text-col">
            Discover the natural and human caused greenhouse gas sources and
            sinks in the map, and know about the air quality around you.
          </p>
        </div>

        <div className="relative w-full h-[30rem] mt-[3rem] slide-left slow-fade-in">
          <img
            src="mmm.jpg"
            className="w-full h-full object-cover"
            alt="Descriptive text"
          />

          {/* GameButton in the center of the image */}

          <div className="absolute inset-0 flex items-center justify-center">
          
          <button className="btn btn-info bg-orange-300">
          {" "}
          <a href="/map">Explore Maps and Data</a>
        </button>
  
          </div>
        </div>
      </div>


          
        </div>
      </div>

      <div className="max-container w-4/5 mx-auto">
        <hr className="my-4 h-[2px] bg-[#e3dddd] border-0" />
      </div>
      <div className="">
        <div className="max-container w-4/5 mx-auto ">
          <h1 className="flex text-col mb-5 xl:flex-row flex-col justify-center items-center font-palanquin lg:text-3xl sm:text-xl lg:leading-[30px] xl:leading-[40px] lg:pt-10 z-10 sm:pt-20 font-bold text-col slow-fade-intitle-bold">
          AR Experience
          </h1>
        </div>

        <div className="flex items-center justify-center text-center">
          <p className="w-4/5 font-montserrat text-slate-gray text-lg mt-6 mb-[1rem] sm-text-col">
          Discover a new dimension with our Augmented Reality experience, where the virtual world blends seamlessly with reality, allowing you to explore, engage, and transform your surroundings like never before!
          </p>
        </div>

        <div className="relative w-full h-[30rem] mt-[3rem] slide-left slow-fade-in">
          <img
            src="lll.jpg"
            className="w-full h-full object-cover"
            alt="Descriptive text"
          />

          {/* GameButton in the center of the image */}

          <div className="absolute inset-0 flex items-center justify-center">
            <GameButton />
          </div>
        </div>
      </div>
      <div className="h-32 w-full"></div>
    </div>
  );
};

export default Home;
