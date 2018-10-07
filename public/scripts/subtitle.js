// Animated subtitle using Typed.js

// Defaults
const TYPE_SPEED = 40;
const BACK_SPEED = 20;


class ItemTyped {

  constructor(options) {
    this.options = {
      typeSpeed: TYPE_SPEED,
      backSpeed: BACK_SPEED,
      strings: [],
      onComplete: () => {},
      ...options,
    };
    this.build();
  }

  build() {
    new Typed(this.options.id, {
      strings: this.options.strings,
      typeSpeed: this.options.typeSpeed,
      backSpeed: this.options.backSpeed,
      onComplete: (self) => {
        self.destroy();
        this.options.onComplete();
      },
    });
  }
}

class Subtitle {

  constructor(options) {
    this.options = {
      typeSpeed: TYPE_SPEED,
      backSpeed: BACK_SPEED,
      backDelay: 200,
      ...options,
    };
    this.build();
  }

  build() {
    let lastPos = 0;
    new Typed(this.options.titleId, {
      strings: this.options.groups.map(group => group.title),
      typeSpeed: this.options.typeSpeed,
      backSpeed: this.options.backSpeed,
      loop: true,
      showCursor: false,
      fadeOut: true,
      backDelay: this.options.backDelay,
      onStringTyped: (pos, self) => {
        if (lastPos === pos) {
          self.toggle();
          this.buildItem(this.options.groups[pos], () => self.toggle())
          lastPos++;
        } else if (lastPos === this.options.groups.length) {
          lastPos = 0;
        }
      },
    });
  }

  buildItem(group, onComplete) {
    new ItemTyped({
      id: this.options.itemId,
      strings: [
        ...group.items.map(item => item + '.'),
        '',  // Final backspace
      ],
      onComplete: () => onComplete(),
    })
  }
}
