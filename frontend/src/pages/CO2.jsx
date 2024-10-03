import React, { useEffect, useState } from "react";
import Phaser from "phaser";
import MessageBox from "../utils/MessageBox.js";
import Button from "../utils/Button.js";
import { useScrollReveal } from "@/components";
import co2 from "/video/co2.mp4";
import "../style/font.css";

class CO2Controller extends Phaser.Scene {
  preload() {
    this.load.image("sky", "sky.png");
    this.load.image("tree", "tree.png");
    this.load.image("factory", "factory.png");
    this.load.image("catPaw", "catPaw.png");
    this.load.spritesheet({
      key: "growingTree",
      url: "growingTree.png",
      frameConfig: {
        frameWidth: 260,
        frameHeight: 245,
        startFrame: 0,
        endFrame: 1,
      },
    });
    this.load.spritesheet({
      key: "growingTree2",
      url: "growingTree2.png",
      frameConfig: {
        frameWidth: 32,
        frameHeight: 21,
        startFrame: 2,
      },
    });
    this.load.spritesheet("car", "car.png", {
      frameWidth: 96,
      frameHeight: 48,
    });

    this.load.spritesheet("catFace1", "catFace1.png", {
      frameWidth: 81.5,
      frameHeight: 38,
    });
    this.load.spritesheet("catFace2", "catFace2.png", {
      frameWidth: 81.5,
      frameHeight: 37,
    });
    this.load.spritesheet("smoke", "smoke.png", {
      frameWidth: 32,
      frameHeight: 32,
    });
    this.load.spritesheet("cycling", "cycling.png", {
      frameWidth: 182.4,
      frameHeight: 136.5,
    });
  }

  create() {
    this.background = this.add.image(0, 0, "sky");
    this.background.setOrigin(0, 0);

    this.widthRatio = 800 / this.background.width;
    this.heightRatio = 300 / this.background.height;

    this.background.setScale(this.widthRatio, this.heightRatio);

    this.add.image(660, 230, "factory").setScale(0.5);
    this.cutTree = this.add.image(500, 290, "tree").setScale(0.1);
    this.anims.create({
      key: "car",
      frames: this.anims.generateFrameNumbers("car"),
      frameRate: 20,
      repeat: -1,
    });
    this.anims.create({
      key: "growingTree",
      frames: this.anims.generateFrameNumbers("growingTree"),
      frameRate: 2,
      repeat: 0,
    });
    this.anims.create({
      key: "growingTree2",
      frames: this.anims.generateFrameNumbers("growingTree2"),
      frameRate: 3,
      repeat: 0,
    });
    this.anims.create({
      key: "smoke",
      frames: this.anims.generateFrameNumbers("smoke"),
      frameRate: 5,
      repeat: -1,
    });
    this.anims.create({
      key: "catFace1",
      frames: this.anims.generateFrameNumbers("catFace1"),
      frameRate: 2,
      repeat: -1,
    });
    this.anims.create({
      key: "catFace2",
      frames: this.anims.generateFrameNumbers("catFace2"),
      frameRate: 5,
      repeat: -1,
    });
    this.anims.create({
      key: "cycling",
      frames: this.anims.generateFrameNumbers("cycling"),
      frameRate: 5,
      repeat: -1,
    });
    this.tree1 = this.add.sprite(380, 250, "growingTree");
    this.tree2 = this.add.sprite(240, 250, "growingTree");
    this.tree3 = this.add.sprite(480, 300, "growingTree2");
    this.car = this.add.sprite(200, 300, "car").play("car");

    this.add.sprite(595, 130, "smoke").play("smoke");
    this.add.rectangle(100, 290, 80, 90, 0xed7f79).setOrigin(0);
    this.add.rectangle(300, 250, 80, 130, 0xffffff).setOrigin(0);

    this.add.sprite(99, 289, "catFace1").play("catFace1").setOrigin(0);
    this.add.image(100, 320, "catPaw").setOrigin(0);
    this.add.sprite(300, 250, "catFace2").play("catFace2").setOrigin(0);
    this.add.image(300, 320, "catPaw").setOrigin(0);
    this.btn1 = new Button({
      ctx: this,
      x: 20,
      y: 230,
      width: 270,
      height: 40,
      btnName: "Choose Green Transport 👈🏻",
    }).createButtons();
    this.btn2 = new Button({
      ctx: this,
      x: 240,
      y: 350,
      width: 200,
      height: 40,
      btnName: "Reforestation 👈🏻",
    }).createButtons();
    this.btn1.visible = this.btn2.visible = false;
    this.btn1.getByName("btn").on("pointerdown", () => {
      this.car.flipX = true;
      this.car.play("cycling").setScale(0.6);
      this.btn1.visible = false;
      this.btn2.visible = true;
    });
    this.btn2.getByName("btn").on("pointerdown", () => {
      this.tree1.play("growingTree");
      this.tree2.play("growingTree");
      this.tree3.play("growingTree2");
      this.cutTree.visible = false;
      this.btn2.visible = false;
    });
    this.converse();
  }
  async converse() {
    await new MessageBox({ x: 40, y: 230, height: 40, ctx: this }).startTyping([
      {
        text: "It is very warm today.",
      },
    ]);
    await new MessageBox({ x: 290, y: 40, height: 200, ctx: this }).startTyping(
      [
        {
          text: "Yeah, it's mostly because of CO₂ in the air. CO₂ is responsible for approximately two-thirds of the warming effect caused by greenhouse gases.",
        },
      ]
    );
    await new MessageBox({ x: 20, y: 230, height: 40, ctx: this }).startTyping([
      {
        text: "CO₂? What causes it?",
      },
    ]);
    await new MessageBox({ x: 290, y: 20, height: 220, ctx: this }).startTyping(
      [
        {
          text: "In power plants, coal and natural gas are burned to produce electricity, releasing CO₂. Cars, trucks, airplanes, and ships that burn gasoline or diesel emit it.",
        },
      ]
    );
    await new MessageBox({ x: 30, y: 210, height: 70, ctx: this }).startTyping([
      {
        text: "Oh... what should we do to stop it?",
      },
    ]);
    await new MessageBox({
      x: 300,
      y: 110,
      height: 120,
      ctx: this,
    }).startTyping([
      {
        text: "we should use cleaner energy like wind and solar, and plant more trees.",
      },
    ]);
    this.btn1.visible = true;
  }
  update() {
    this.car.x += 2;
    if (this.car.x > this.scale.width) {
      this.car.x = -this.car.width;
    }
  }
}
const CO2 = () => {
  useScrollReveal();
  const config = {
    type: Phaser.AUTO,
    parent: "phaser-container",
    width: 800,
    height: 400,
    scene: CO2Controller,
    backgroundColor: "#fca44a",
    physics: {
      default: "arcade",
      arcade: {
        gravity: { y: 200 },
      },
    },
  };

  const [currentSlide, setCurrentSlide] = useState(0);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [game, setGame] = useState(null); // State to hold the Phaser game instance

  const handleTopicClick = (index) => {
    setSelectedTopic(index);
  };

  const handleBackClick = () => {
    setSelectedTopic(null);
  };
  const slides = [
    {
      title: "Transportation Sector",
      content:
        "Vehicles powered by gasoline and diesel, including cars, trucks, airplanes, and ships, are major contributors to CO₂ emissions. The combustion of fossil fuels in engines directly releases CO₂ into the atmosphere.",
    },
    {
      title: "Power Generation",
      content:
        "Power plants that burn coal, oil, or natural gas to produce electricity release significant amounts of CO₂. Fossil fuel combustion for electricity and heat generation is a leading driver of global emissions.",
    },
    {
      title: "Agriculture",
      content:
        "While agriculture primarily emits methane (CH₄) and nitrous oxide (N₂O), CO₂ is also released during the production and use of energy-intensive fertilizers, machinery operation, and the clearing of land for farming.",
    },
    {
      title: "Land Use and Deforestation",
      content: `Deforestation significantly contributes to CO₂ emissions by reducing forests that naturally absorb carbon dioxide, while also releasing stored carbon into the atmosphere. Studies show that about 23% of global emissions are tied to land-use changes, with deforestation accounting for half of these emissions.`,
    },
    {
      title: "Waste Management",
      content:
        "The decomposition of organic materials in landfills produces carbon dioxide and methane, particularly when waste is not properly managed or landfills lack adequate methane capture systems.",
    },
    {
      title: "Oil and Gas Industry",
      content:
        "The extraction, refining, and distribution of oil and natural gas release CO₂ through flaring, venting, and leakage. These processes, along with the burning of fossil fuels for energy, are significant contributors to CO₂ emissions",
    },
  ];
  const topics = [
    {
      title: "Transportation Sector",
      content: [
        {
          sub: "Transition to Electric Vehicles (EVs)",
          con: "Promoting the use of electric vehicles can significantly reduce CO₂ emissions. Governments can incentivize EV adoption through subsidies, tax breaks, and developing charging infrastructure.",
        },
        {
          sub: "Public Transportation Improvements",
          con: "Investing in public transit systems can decrease the number of individual cars on the road, reducing overall emissions. Encouraging carpooling and biking can also be effective.",
        },
        {
          sub: "Research & Programs",
          con: "The NASA Earth Science Division is involved in studying transportation emissions through satellite observations, which can inform policies to reduce emissions from this sector.",
        },
      ],
      imgSrc: "bicycle.jpeg",
    },
    {
      title: "Power Generation",
      content: [
        {
          sub: "Renewable Energy Adoption",
          con: "Transitioning from fossil fuels to renewable sources like solar, wind, and hydroelectric power can drastically cut emissions. Governments can implement policies that encourage investment in renewable energy technologies.",
        },
        {
          sub: "Energy Efficiency Improvements",
          con: "Upgrading power plants to be more energy-efficient and implementing smart grid technology can reduce emissions associated with power generation.",
        },
      ],
      imgSrc: "renewable.jpeg",
    },
    {
      title: "Agriculture",
      content: [
        {
          sub: "Sustainable Farming Practices",
          con: "Implementing practices such as crop rotation, agroforestry, and cover cropping can enhance soil carbon storage and reduce reliance on synthetic fertilizers.",
        },
        {
          sub: "Precision Agriculture",
          con: "Utilizing technology to optimize input usage can minimize emissions from fertilizers and machinery.",
        },
      ],
      imgSrc: "agriculture.jpeg",
    },
    {
      title: "Land Use and Deforestation",
      content: [
        {
          sub: "Reforestation and Afforestation",
          con: "Initiatives that promote planting trees and restoring forests can sequester CO₂. Programs should focus on conserving existing forests to maintain their carbon storage capabilities.",
        },
        {
          sub: "Sustainable Land Management",
          con: "Encouraging practices that improve land use efficiency can reduce the need for deforestation.",
        },
      ],
      imgSrc: "deforestation.jpeg",
    },
    {
      title: "Waste Management",
      content: [
        {
          sub: "Improved Waste Segregation and Recycling",
          con: "Enhancing recycling programs and promoting waste reduction can minimize the amount of organic waste sent to landfills, thereby reducing methane and CO₂ emissions.",
        },
        {
          sub: "Landfill Gas Capture Systems",
          con: "Installing systems that capture methane emissions from landfills can significantly decrease greenhouse gas emissions.",
        },
      ],
      imgSrc: "recycle.jpeg",
    },
    {
      title: "Oil and Gas Industry",
      content: [
        {
          sub: "Implementing Carbon Capture and Storage (CCS)",
          con: "This technology captures CO₂ emissions from industrial processes and stores it underground, preventing it from entering the atmosphere.",
        },
        {
          sub: "Leak Detection and Repair Programs",
          con: "Strengthening regulations for monitoring and repairing leaks during extraction and distribution can significantly reduce emissions.",
        },
      ],
      imgSrc: "oil.jpeg",
    },
  ];

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
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

  return (
    <div
      className="slide-up flex flex-col p-0 items-center justify-center text-center text-[#67754a]"
      style={{ backgroundImage: "url('oil3.jpg')" }}
    >
      <h1 className="text-xl font-bold md:text-2xl lg:text-[2rem] font-palanquin mb-3 mt-5 justify-center text-center">
        Understanding Carbon Dioxide (CO₂) Emissions
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
      <div
        id="phaser-container"
        style={{
          width: "800px",
          // position: "relative",
          margin: "20px auto",
        }}
      />
      <div
        className="container"
        style={{ marginLeft: "0 !important", marginRight: "0 !important" }}
      >
        <div className="row bg-[#7d8b60] style={{ margin: 0, padding: 0 }} ">
          <div
            className="w-full md:w-1/2  text-white"
            style={{ position: "relative", padding: 0 }}
          >
            <video
              src={co2}
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
                bottom: "0",
                left: "0",
                paddingTop: "80px",
                paddingRight: "20px",
              }}
            >
              <h1 className="subtitle-bold px-3 text-end">
                Do you know what causes carbon dioxide(CO2) emission?
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
              <div className="controls text-center">
                <button
                  onClick={prevSlide}
                  className="btn  border-white text-white mr-5 hover:bg-white/20"
                  style={{ borderRadius: "10px 0px 10px 0px" }}
                >
                  Prev
                </button>
                <button
                  onClick={nextSlide}
                  className="btn  border-white text-white mr-5 hover:bg-white/20"
                  style={{ borderRadius: "10px 0px 10px 0px" }}
                >
                  Next
                </button>
              </div>
            </div>
          </div>
        </div>
        <div
          className="row"
          style={{
            width: "100%",
            backgroundColor: "white",
          }}
        >
          <div className="col-sm-12">
            <h1 className="title-normal mt-20 text-black">
              What are the solutions?
            </h1>
            <p className="text-gray">
              CO2 acts like a thickening blanket around the Earth, trapping heat
              and warming the planet. But we’ve got the power to outsmart it! 🌍
            </p>
          </div>
        </div>
        <div
          className="row p-20"
          style={{
            backgroundColor: "white",
          }}
        >
          {selectedTopic === null ? (
            <div className="grid text-black">
              {topics.map((topic, index) => (
                <div
                  className="grid-item text-center"
                  key={index}
                  onClick={() => handleTopicClick(index)}
                >
                  <img src={topic.imgSrc} alt={topic.title} />
                  <b>{topic.title}</b>
                </div>
              ))}
            </div>
          ) : (
            <div className="expanded-content text-black">
              <div className="row">
                <div className="col-sm-7 text-black text-start para">
                  <h1 className="subtitle-bold text-black">
                    {topics[selectedTopic].title}
                  </h1>
                  {topics[selectedTopic].content.map((subTopic) => {
                    return (
                      <>
                        <p>
                          <b>{subTopic.sub}:</b> {subTopic.con}
                        </p>
                        <br />
                      </>
                    );
                  })}
                </div>
                <div className="col-sm-5">
                  <img
                    src={topics[selectedTopic].imgSrc}
                    alt="bicycle"
                    style={{ width: "80%", margin: "auto" }}
                  />
                </div>
              </div>
              <button
                type="button"
                className="btn btn-primary"
                onClick={handleBackClick}
              >
                Back
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CO2;
