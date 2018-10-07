const LIGHT_THEME_PROPERTIES = {
  ['--color-accent']: '#556269',
  ['--color-text']: '#354249',
  ['--color-bg']: '#dcf4f1',
  ['--color-bg-dark']: '#bcd4d1',
  ['--color-muted']: '#556269',
};

const DARK_THEME_PROPERTIES = {
  ['--color-accent']: 'white',
  ['--color-text']: '#8fc1ba',
  ['--color-bg']: '#354249',
  ['--color-bg-dark']: '#2c373d',
  ['--color-muted']: '#dcf4f1',
}

const THEME_KEY = 'theme';
const DEFAULT_THEME = 'dark';

class ThemeToggler {

  constructor() {
    this.setTheme(this.getInitialTheme());
  }

  getInitialTheme() {
    return localStorage.getItem(THEME_KEY) || DEFAULT_THEME;
  }

  getThemeProperties() {
    return this.theme === 'dark' ? DARK_THEME_PROPERTIES : LIGHT_THEME_PROPERTIES;
  }

  setTheme(value) {
    this.theme = value;
    localStorage.setItem(THEME_KEY, value);
    const properties = this.getThemeProperties();
    Object.keys(properties).forEach((key) => {
      document.body.style.setProperty(key, properties[key]);
    });
  }

  toggle() {
    this.setTheme(this.theme === 'dark' ? 'light' : 'dark');
  }
}

function listenToggleTheme(elementId) {
  const toggler = new ThemeToggler();
  const element = document.querySelector(elementId);
  element.onclick = () => toggler.toggle();
}
