import React, { useEffect } from "react";
import Phaser from "phaser";
import MessageBox from "../utils/MessageBox.js";
import { useScrollReveal } from "@/components/index.js";
class Example extends Phaser.Scene {
  preload() {
    this.load.image("fluorinate", "fluorinate.png");
    this.load.image("spray", "spray.png");
    this.load.image("catPaw", "catPaw.png");
    this.load.spritesheet("air_conditioner", "air_conditioner2.png", {
      frameWidth: 90.75,
      frameHeight: 38,
    });
    this.load.spritesheet("catFace1", "catFace1.png", {
      frameWidth: 81.5,
      frameHeight: 38,
    });
    this.load.spritesheet("catFace2", "catFace2.png", {
      frameWidth: 81.5,
      frameHeight: 37,
    });
  }

  create() {
    this.background = this.add.image(0, 0, "fluorinate");
    this.background.setOrigin(0, 0);

    this.widthRatio = 800 / this.background.width;
    this.heightRatio = 400 / this.background.height;

    this.background.setScale(this.widthRatio, this.heightRatio);
    this.add.image(270, 230, "spray").setScale(0.1);
    this.anims.create({
      key: "air_conditioner",
      frames: this.anims.generateFrameNumbers("air_conditioner"),
      frameRate: 2,
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
    this.add.sprite(105, 70, "air_conditioner").play("air_conditioner");
    this.add.rectangle(100, 290, 80, 90, 0xed7f79).setOrigin(0);
    this.add.rectangle(350, 250, 80, 130, 0xffffff).setOrigin(0);

    this.add.sprite(99, 289, "catFace1").play("catFace1").setOrigin(0);
    this.add.image(100, 320, "catPaw").setOrigin(0);
    this.add.sprite(350, 250, "catFace2").play("catFace2").setOrigin(0);
    this.add.image(350, 320, "catPaw").setOrigin(0);
    this.converse();
  }
  async converse() {
    await new MessageBox({ x: 40, y: 230, height: 40, ctx: this }).startTyping([
      {
        text: "it’s so warm outside!",
      },
    ]);
    await new MessageBox({
      x: 340,
      y: 120,
      height: 120,
      ctx: this,
    }).startTyping([
      {
        text: "Meee-yow... Yeah, it’s because of that fridge, the air conditioner, and even the aerosol can.",
      },
    ]);
    await new MessageBox({ x: 30, y: 210, height: 70, ctx: this }).startTyping([
      {
        text: "Wait, how do they make it warm?",
      },
    ]);
    await new MessageBox({ x: 440, y: 10, height: 220, ctx: this }).startTyping(
      [
        {
          text: "They leak fluorinated gases, like HFCs. Those gases get into the air when they’re not maintained properly or when we use certain products, like aerosols.",
        },
      ]
    );
    await new MessageBox({
      x: 340,
      y: 110,
      height: 120,
      ctx: this,
    }).startTyping([
      {
        text: "They trap heat in the atmosphere, way more than CO₂, making the planet hotter.",
      },
    ]);
    await new MessageBox({
      x: 40,
      y: 230,
      width: 220,
      height: 40,
      ctx: this,
    }).startTyping([
      {
        text: "What can we do about it?",
      },
    ]);
    await new MessageBox({ x: 340, y: 80, height: 150, ctx: this }).startTyping(
      [
        {
          text: "Use more eco-friendly alternatives, fix leaks, and stop using harmful sprays. That’ll help reduce the emissions.",
        },
      ]
    );
  }
}
const Fluorinates = () => {
  useScrollReveal();
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
    const game = new Phaser.Game(config);


    return () => {
      game.destroy(true);
    };
  }, []);

  return (
    <div className="slide-up flex flex-col p-0 items-center justify-center text-center text-[#67754a]"> 
    <h1 className="text-xl md:text-2xl lg:text-[2rem] font-bold font-palanquin mb-3 mt-5 justify-center text-center">
      Have You Heard About the Power of Fluorinated Gases?
    </h1>
    <div
      id="phaser-container"
      style={{ width: "800px", position: "relative", margin: "20px auto" }}
    />
    <div className="max-w-[800px] px-4"> 
      <p className="leading-relaxed">
        Fluorinated gases may not be as well-known, but they pack a serious punch when it comes to trapping heat! 🌡️ Found in things like refrigerators and air conditioners, these gases can stay in the atmosphere for a long time. But don’t worry—we can make a difference! By properly maintaining appliances and choosing greener alternatives, we can help reduce these gases. 🌍 Ready to step up and cool down the planet? Let’s get started! 🌱♻️ Press "Enter" to dive into the comic!
      </p>
    </div>
    
    <div className="h-32"></div>
    </div>
  );
};

export default Fluorinates;
