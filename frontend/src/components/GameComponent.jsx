import React, { useEffect } from "react";
import Phaser from "phaser";

const GameComponent = ({ config }) => {
  useEffect(() => {
    const game = new Phaser.Game(config);

    return () => {
      game.destroy(true);
    };
  }, []);

  return (
    <div
      id="phaser-container"
      style={{ width: "800px", position: "relative", margin: "20px auto" }}
    />
  );
};

export default GameComponent;
