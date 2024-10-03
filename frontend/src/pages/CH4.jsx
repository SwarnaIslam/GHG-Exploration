import React, { useState, useEffect } from "react";
import Phaser from "phaser";
import MessageBox from "../utils/MessageBox.js";
import { useScrollReveal } from "@/components/index.js";
import ch4 from "/video/ch4.mp4";

class Example extends Phaser.Scene {
  preload() {
    this.load.image("ch4", "ch4.png");
    this.load.image("char1", "char1.png");
    this.load.image("char2", "char2.png");
  }

  create() {
    this.background = this.add.image(0, 0, "ch4");
    this.background.setOrigin(0, 0);

    this.widthRatio = 800 / this.background.width;
    this.heightRatio = 400 / this.background.height;

    this.background.setScale(this.heightRatio);
    this.char1 = this.add.image(100, 260, "char1");
    this.char1.setScale(0.5);
    this.char1.setOrigin(0);

    this.char2 = this.add.image(400, 240, "char2");
    this.char2.setScale(0.5);
    this.char2.setOrigin(0);
    this.converse();
  }

  async converse() {
    await new MessageBox({ x: 90, y: 30, height: 220, ctx: this }).startTyping([
      {
        text: "Methane escapes into the air during the extraction and transportation of oil and natural gas. is there a way to stop the leaking?",
      },
    ]);
    await new MessageBox({ x: 390, y: 30, height: 220, ctx: this }).startTyping(
      [
        {
          text: "We can establish comprehensive Leak Detection and Repair (LDAR) Programs to monitor emissions continuously and ensure prompt repairs of any detected leaks.",
        },
      ]
    );
    await new MessageBox({ x: 390, y: 30, height: 220, ctx: this }).startTyping(
      [
        {
          text: "Also we should replace aging infrastructure with newer, more reliable materials and designs that are less likely to leak.",
        },
      ]
    );
    await new MessageBox({ x: 90, y: 130, height: 120, ctx: this }).startTyping(
      [
        {
          text: "...",
          speed: 800,
        },
        {
          text: "Does methane emission only happen during leaking?",
        },
      ]
    );
    await new MessageBox({ x: 490, y: 30, height: 220, ctx: this }).startTyping(
      [
        {
          text: "No. When food waste and other organic materials break down in landfills, they release methane. Manure piles from farms release methane as they decompose.",
        },
      ]
    );
    await new MessageBox({ x: 90, y: 170, height: 80, ctx: this }).startTyping([
      {
        text: "!!!!!!!!!!",
        speed: 10,
      },
      {
        text: "What should we do then to solve it?",
        speed: 20,
      },
    ]);
    await new MessageBox({ x: 490, y: 30, height: 220, ctx: this }).startTyping(
      [
        {
          text: "Instead of throwing food scraps in the trash, compost them at home or use a local composting service to reduce landfill methane.",
        },
      ]
    );
    await new MessageBox({
      x: 490,
      y: 130,
      height: 120,
      ctx: this,
    }).startTyping([
      {
        text: "Support farms that use manure for biogas production, turning waste into energy.",
      },
    ]);
  }
}

const CH4 = () => {
  useScrollReveal();
  const [currentSlide, setCurrentSlide] = useState(0);
  const [game, setGame] = useState(null); // State to hold the Phaser game instance
  const config = {
    type: Phaser.AUTO,
    parent: "phaser-container",
    width: 800,
    height: 400,
    scene: Example,
    physics: {
      default: "arcade",
      arcade: {
        gravity: { y: 200 },
      },
    },
  };

  useEffect(() => {
    const newGame = new Phaser.Game(config);
    setGame(newGame); // Store the game instance in state

    return () => {
      newGame.destroy(true);
    };
  }, []);

  const rerunGame = () => {
    if (game) {
      game.destroy(true); // Destroy the current game instance
    }
    const newGame = new Phaser.Game(config); // Create a new game instance
    setGame(newGame); // Update state with new game instance
  };

  const slides = [
    {
      title: "Fossil Fuel Production and Use",
      content:
        " Methane is released during the extraction, processing, and transportation of oil and natural gas. Leaks from pipelines and equipment contribute significantly to methane emissions.",
    },
    {
      title: "Agriculture",
      content:
        "Methane is produced as a byproduct of digestion in ruminant animals like cows, sheep, and goats. The gas is released mainly through belching.",
    },
    {
      title: "Landfills",
      content:
        "Methane is produced by the anaerobic decomposition of organic waste in landfills. It is one of the major sources of anthropogenic methane.",
    },
    {
      title: "Wetlands",
      content: `Wetlands release methane during the anaerobic decomposition of organic matter. The extent of these emissions depends on water levels, temperature, and the type of vegetation.`,
    },
    {
      title: "Permafrost Thawing",
      content:
        "As permafrost in Arctic regions thaws due to warming temperatures, methane trapped in frozen organic material is released into the atmosphere.",
    },
  ];

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  return (
    <div className="slide-up flex flex-col p-0 items-center justify-center text-center text-[#67754a]">
      <h1 className="text-xl md:text-2xl lg:text-[2rem] font-bold font-palanquin mb-3 mt-5 justify-center text-center">
        Understanding Methane Emissions
      </h1>
      <p className="w-4/5 text-center"> Press Enter to run the comic.</p>
      <div
        id="phaser-container"
        className=" mb-3 "
        style={{
          width: "800px",
          margin: "20px auto",
        }}
      />
      <button
        onClick={rerunGame}
        className="btn btn-outline-secondary ml-5 mb-5 w-[6rem] text-[#4f5c34] hover:bg-[#A1B770]"
        style={{ borderRadius: "10px" }}
      >
        Rerun
      </button>
      <div
        className="container"
        style={{ marginLeft: "0 !important", marginRight: "0 !important" }}
      >
        <div className="row  bg-[#7d8b60] style={{ margin: 0, padding: 0 }} ">
          <div
            className="w-full md:w-1/2  text-white"
            style={{ position: "relative", padding: 0 }}
          >
            <video
              src={ch4}
              autoPlay
              loop
              muted
              style={{ width: "100%", height: "100%", objectFit: "cover" }}
            />
            <div
              className="content"
              style={{
                position: "absolute",
                top: "0",
                right: "0",
                left: "0",
                paddingTop: "30px",
              }}
            >
              <h1 className="subtitle-bold px-3 text-center">
                Do you know what causes Methane(CH4) emission?
              </h1>
            </div>
          </div>
          <div className="w-full md:w-1/2  bg-[#7d8b60] style={{ padding: 0 }} ">
            <div className="text-slider">
              <div
                className="text-content text-start px-5 py-5"
                style={{ minHeight: "150px" }}
              >
                <h1 className="font-bold text-2xl mb-2 text-white">
                  {slides[currentSlide].title}
                </h1>
                <p className="para text-white">
                  {slides[currentSlide].content}
                </p>
              </div>
              <div className="controls text-center ">
                <button
                  onClick={prevSlide}
                  className="btn border-white text-white mr-5 hover:bg-white/20"
                  style={{ borderRadius: "10px 0px 10px 0px" }}
                >
                  Prev
                </button>
                <button
                  onClick={nextSlide}
                  className="btn border-white text-white mr-5 hover:bg-white/20"
                  style={{ borderRadius: "10px 0px 10px 0px" }}
                >
                  Next
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="h-[3.4rem]"></div>
    </div>
  );
};

export default CH4;
