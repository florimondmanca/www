const groups = [
  {
    title: 'I enjoy',
    items: [
      'sharing knowledge',
      'writing code',
      'building things',
      'solving problems',
      'working with people',
    ],
  },
  {
    title: 'I write about',
    items: [
      'technology',
      'software engineering',
      'stream processing',
      'web development',
      'programming',
    ],
  },
  {
    title: 'I am',
    items: [
      'curious and passionate',
      'French and Belgian',
      'a Master of Engineering student',
      'a bit of an idealist',
    ]
  },
  {
    title: 'I build stuff using',
    items: [
      'Python',
      'Django',
      'JavaScript',
      'Angular',
      'Docker',
      'TravisCI',
      'AWS',
      'Apache Kafka',
      'SQL databases',
      'brainpower',
    ]
  }
];

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
      groups: [],
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
        } else if (lastPos === groups.length) {
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
        // Final backspace
        '',
      ],
      onComplete: () => onComplete(),
    })
  }
}
