class Button {
  constructor(config) {
    this.ctx = config.ctx;
    this.x = config.x || 0;
    this.y = config.y || 0;
    this.btnName = config.btnName || "";
    this.width = config.width || 200;
    this.height = config.height || 50;
    this.btnColor = config.btnColor || 0x000000;
    this.fontColor = config.fontColor || "#ffffff";
    this.fontSize = config.fontSize || 10;
    this.borderColor = config.borderColor || 0x008483;
    this.borderThick = config.borderThick || 1;
  }
  createButtons() {
    const btnContainer = this.ctx.add.container(this.x, this.y);
    const btnBg = this.ctx.add.rectangle(
      0,
      0,
      this.width,
      this.height,
      this.btnColor
    );

    const graphics = this.ctx.add.graphics();
    graphics.lineStyle(this.borderThick, this.borderColor);
    graphics.strokeRect(0, 0, this.width, this.height);

    const mask = this.ctx.add
      .rectangle(0, 0, this.width, this.height, 0xc3dc56, 0)
      .setName("btn");
    const text = this.ctx.add.text(
      this.width / 2,
      this.height / 2,
      this.btnName,
      {
        font: `${this.fontSize}px PressStart`,
        fill: this.fontColor,
        align: "center",
      }
    );
    text.setOrigin(0.5);
    btnBg.setOrigin(0);

    btnContainer.add(graphics);
    btnContainer.add(btnBg);
    btnContainer.add(text);
    btnContainer.add(mask);

    mask.setInteractive({ cursor: "pointer" });
    mask.setOrigin(0);

    mask.on("pointerover", () => {
      btnBg.setFillStyle(0xffffff);
      text.setColor("#000000");
    });
    mask.on("pointerout", () => {
      btnBg.setFillStyle(this.btnColor);
      text.setColor(this.fontColor);
    });
    return btnContainer;
  }
}
export default Button;
