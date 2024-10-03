class MessageBox {
  constructor(con) {
    const width = con.width || 200;
    const height = con.height || 150;

    const x = con.x;
    const y = con.y;

    this.ctx = con.ctx;
    this.messageDisplayed = false;
    this.text = "";

    this.messageBox = this.ctx.add.container(x, y);

    if (!con.transparent) {
      const graphics = this.ctx.add.graphics();
      graphics.fillStyle(0xfff2f9, 1);
      graphics.lineStyle(4, 0x1f4685);
      graphics.fillRoundedRect(0, 0, width, height, 0);
      graphics.strokeRoundedRect(0, 0, width, height, 0);
      this.messageBox.add(graphics);
    }
    this.messageBox.visible = true;

    this.messageText = this.ctx.add.text(10, 10, "", {
      fontFamily: con.fontFamily || "Quantico",
      fontSize: con.fontSize || 20,
      color: con.fontColor || "#1F4685",
      wordWrap: {
        width: width - 10,
      },
    });
    this.messageText.setLineSpacing(5);
    this.messageText.setOrigin(0, 0);

    this.messageBox.add(this.messageText, 0, 0);

    this.ctx.input.keyboard.on("keydown-ENTER", () => {
      this.messageDisplayed = true;
    });
  }

  startTyping(message) {
    if (this.ctx.countdown) {
      this.ctx.countdown.pause();
    }
    this.message = message;
    this.ctx.input.enabled = false;
    let line = [];

    for (let i = 0; i < this.message.length; i++) {
      let text = this.message[i].text;
      let delay = this.message[i].speed || 40;
      text.split("").forEach((character) => {
        if (character === " ") {
          line.push({ character: " ", delay: 0 });
        } else {
          line.push({ character, delay });
        }
      });
      if (i < this.message.length - 1) {
        line.push({ character: " ", delay: 0 });
      }
    }
    return new Promise((resolve) => {
      this.revealText(line, resolve);
    });
  }
  revealText(line, resolve) {
    let next = line.splice(0, 1)[0];
    this.text += next.character;

    this.messageText.setText(this.text);
    if (line.length === 0 || this.messageDisplayed) {
      for (let i = 0; i < line.length; i++) this.text += line[i].character;
      this.messageText.setText(this.text);
      if (this.ctx.countdown) {
        this.ctx.countdown.resume();
      }
      this.ctx.input.keyboard.on(
        "keydown",
        this.removeMessageBox.bind(this, resolve)
      );
    } else {
      setTimeout(() => {
        this.revealText(line, resolve);
      }, next.delay);
    }
  }
  removeMessageBox(resolve, event) {
    if (event.code == "Enter") {
      this.messageBox.destroy();
      this.ctx.input.keyboard.off("keydown", this.removeMessageBox, this);
      this.ctx.input.enabled = true;
      resolve();
    }
  }
}
export default MessageBox;
